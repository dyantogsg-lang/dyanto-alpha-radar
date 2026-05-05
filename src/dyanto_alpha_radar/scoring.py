from __future__ import annotations


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def _num(pair: dict, key: str, default: float = 0) -> float:
    try:
        return float(pair.get(key) or default)
    except (TypeError, ValueError):
        return default


def score_market(pair: dict) -> dict:
    liquidity = _num(pair, "liquidity_usd")
    volume = _num(pair, "volume_24h")
    fdv = _num(pair, "fdv")
    buys = _num(pair, "txns_24h_buys")
    sells = _num(pair, "txns_24h_sells")
    pc1h = _num(pair, "price_change_1h")
    pc24h = _num(pair, "price_change_24h")

    vol_liq = volume / liquidity if liquidity > 0 else 0
    vol_fdv = volume / fdv if fdv > 0 else 0
    buy_ratio = buys / max(buys + sells, 1)

    liquidity_score = clamp((liquidity / 50_000) * 100)
    volume_score = clamp((vol_liq / 12) * 100)
    breadth_score = clamp(((buys + sells) / 1200) * 100)
    pressure_score = clamp((buy_ratio - 0.38) / 0.27 * 100)
    momentum_score = clamp((pc1h * 2.0) + (pc24h * 0.35) + 35)
    valuation_turnover_score = clamp((vol_fdv / 1.2) * 100)

    opportunity = clamp(
        liquidity_score * 0.20
        + volume_score * 0.22
        + breadth_score * 0.18
        + pressure_score * 0.17
        + momentum_score * 0.15
        + valuation_turnover_score * 0.08
    )

    flags: list[str] = []
    risk = 25.0
    if liquidity < 15_000:
        risk += 35
        flags.append("Thin liquidity: pool can move violently or be rugged")
    if vol_liq > 25:
        risk += 22
        flags.append("Overheated volume/liquidity churn")
    elif vol_liq > 12:
        risk += 10
        flags.append("High volume/liquidity")
    if buy_ratio < 0.45:
        risk += 20
        flags.append("Sell pressure exceeds healthy accumulation")
    if pc24h > 180 and liquidity < 30_000:
        risk += 15
        flags.append("Parabolic move on shallow liquidity")
    if fdv and liquidity / fdv < 0.03:
        risk += 8
        flags.append("Low liquidity-to-FDV support")
    if pc1h < -15:
        risk += 12
        flags.append("Short-term reversal pressure")

    risk = clamp(risk)
    if risk >= 85:
        label = "AVOID"
    elif risk >= 72:
        label = "RISKY"
    elif opportunity >= 82:
        label = "HOT"
    elif opportunity >= 68:
        label = "WARM+"
    elif opportunity >= 52:
        label = "WARM"
    else:
        label = "MONITOR"

    return {
        "opportunity_score": round(opportunity, 1),
        "risk_score": round(risk, 1),
        "label": label,
        "vol_liq": round(vol_liq, 2),
        "vol_fdv": round(vol_fdv, 2),
        "buy_ratio": round(buy_ratio, 3),
        "subscores": {
            "liquidity": round(liquidity_score, 1),
            "volume": round(volume_score, 1),
            "breadth": round(breadth_score, 1),
            "buy_pressure": round(pressure_score, 1),
            "momentum": round(momentum_score, 1),
            "valuation_turnover": round(valuation_turnover_score, 1),
        },
        "flags": flags or ["No critical market-structure flag detected"],
    }


def classify_verdict(signals: dict) -> str:
    market = signals.get("market_score", {})
    opportunity = float(market.get("opportunity_score", 0))
    risk = float(market.get("risk_score", 100))
    social = float(signals.get("social_score", 0))
    holder_risk = float(signals.get("holder_risk", 50))
    early_cluster = bool(signals.get("early_wallet_cluster", False))

    if holder_risk >= 78 or (risk >= 82 and social < 35):
        return "Manipulated"
    if early_cluster and social >= 45:
        return "Mixed"
    if social >= 65 and opportunity >= 60 and holder_risk < 60:
        return "Organic"
    if early_cluster or holder_risk >= 62:
        return "Coordinated"
    return "Mixed" if opportunity >= 55 else "Monitor"
