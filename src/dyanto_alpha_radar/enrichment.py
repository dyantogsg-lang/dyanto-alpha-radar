from __future__ import annotations

from datetime import datetime, timezone


def _num(pair: dict, key: str, default: float = 0) -> float:
    try:
        return float(pair.get(key) or default)
    except (TypeError, ValueError):
        return default


def _age_label(pair_created_at) -> str:
    if not pair_created_at:
        return "unknown"
    try:
        ts = float(pair_created_at)
        if ts > 10_000_000_000:
            ts = ts / 1000
        created = datetime.fromtimestamp(ts, tz=timezone.utc)
        hours = max((datetime.now(timezone.utc) - created).total_seconds() / 3600, 0)
        if hours < 1:
            return f"{int(hours * 60)}m"
        if hours < 48:
            return f"{hours:.1f}h"
        return f"{hours / 24:.1f}d"
    except (TypeError, ValueError, OSError):
        return "unknown"


def _status(value: float, warn: float, danger: float, inverted: bool = False) -> str:
    if inverted:
        if value <= danger:
            return "danger"
        if value <= warn:
            return "watch"
        return "ok"
    if value >= danger:
        return "danger"
    if value >= warn:
        return "watch"
    return "ok"


def build_gmgn_style_details(pair: dict, score: dict, pair_count: int, social_score: float) -> dict:
    """Build GMGN-inspired detail panels from public/free data.

    This does not call GMGN private APIs. It mirrors useful concepts: security checks,
    pool profile, timeframe tape, holder/smart-money placeholders, and analyst checklist.
    """
    liquidity = _num(pair, "liquidity_usd")
    volume24 = _num(pair, "volume_24h")
    fdv = _num(pair, "fdv")
    buys24 = _num(pair, "txns_24h_buys")
    sells24 = _num(pair, "txns_24h_sells")
    vol_liq = float(score.get("vol_liq") or (volume24 / liquidity if liquidity else 0))
    buy_ratio = float(score.get("buy_ratio") or (buys24 / max(buys24 + sells24, 1)))
    liq_fdv = liquidity / fdv if fdv else 0
    raw = pair.get("raw") or {}
    boosts = raw.get("boosts") or {}
    labels = raw.get("labels") or []

    liquidity_status = "deep" if liquidity >= 100_000 else "healthy" if liquidity >= 30_000 else "thin"
    sell_pressure = "elevated" if buy_ratio < 0.45 else "balanced" if buy_ratio < 0.58 else "buy-dominant"
    churn_status = _status(vol_liq, warn=12, danger=25)
    liq_support = _status(liq_fdv, warn=0.06, danger=0.025, inverted=True) if fdv else "unknown"

    security_flags: list[str] = []
    if liquidity_status == "thin":
        security_flags.append("Thin liquidity: slippage/rug sensitivity high")
    if churn_status == "danger":
        security_flags.append("Overheated volume/liquidity churn")
    if sell_pressure == "elevated":
        security_flags.append("Seller pressure above healthy accumulation zone")
    if liq_support in {"danger", "watch"}:
        security_flags.append("Low liquidity support versus FDV")
    if pair_count > 3:
        security_flags.append("Multiple pools detected; verify real pool versus dust pools")
    if not security_flags:
        security_flags.append("No critical public-data security flag detected")

    smart_signal = "watch"
    if social_score >= 60 and buy_ratio >= 0.52 and churn_status != "danger":
        smart_signal = "neutral"
    if social_score < 35 or churn_status == "danger" or sell_pressure == "elevated":
        smart_signal = "weak"

    return {
        "security": {
            "liquidity_status": liquidity_status,
            "sell_pressure": sell_pressure,
            "churn_status": churn_status,
            "liquidity_fdv_status": liq_support,
            "honeypot_check": "not_applicable_public_dex_data",
            "renounced_check": "unresolved_without_chain_specific_contract_scan",
            "lp_burn_check": "unresolved_without_pool_authority_scan",
            "flags": security_flags,
        },
        "pool": {
            "dex": pair.get("dex") or "unknown",
            "pair_address": pair.get("pair_address") or "",
            "pair_age": _age_label(pair.get("pair_created_at")),
            "liquidity_usd": liquidity,
            "volume_liquidity_ratio": round(vol_liq, 2),
            "liquidity_fdv_ratio": round(liq_fdv, 4),
            "active_pool_count": pair_count,
            "url": pair.get("url") or "",
        },
        "timeframes": {
            "m5": {
                "price_change_pct": _num(pair, "price_change_5m"),
                "volume_usd": _num(pair, "volume_5m"),
            },
            "h1": {
                "price_change_pct": _num(pair, "price_change_1h"),
                "volume_usd": _num(pair, "volume_1h"),
                "buys": _num(pair, "txns_1h_buys"),
                "sells": _num(pair, "txns_1h_sells"),
            },
            "h6": {
                "price_change_pct": _num(pair, "price_change_6h"),
                "volume_usd": _num(pair, "volume_6h"),
            },
            "h24": {
                "price_change_pct": _num(pair, "price_change_24h"),
                "volume_usd": volume24,
                "buys": buys24,
                "sells": sells24,
            },
        },
        "smart_money": {
            "signal": smart_signal,
            "smart_degen_count": "pending_wallet_enrichment",
            "kol_exposure": "pending_social_enrichment",
            "fresh_wallet_risk": "pending_first_buyer_scan",
            "sniper_risk": "pending_first_buyer_scan",
            "interpretation": "GMGN-like wallet tags require holder/trader enrichment; current signal is inferred from public market structure.",
        },
        "holder_snapshot": {
            "top_holders": "pending_solana_rpc_or_indexer",
            "dev_wallet": "pending_creator_scan",
            "lp_pool_authority": "pending_pool_authority_scan",
            "concentration_risk": "unresolved",
        },
        "discovery": {
            "labels": labels,
            "boosts_active": boosts.get("active", 0),
            "social_score": social_score,
            "source_note": "Dexscreener public data with GMGN-inspired analytical layout",
        },
        "research_checklist": [
            "Check first 70 buyers for sniper/bundler/dev/fresh-wallet clustering",
            "Separate LP/pool authority inventory from real insiders before judging holder risk",
            "Verify liquidity burn/lock and pool authority where chain data is available",
            "Track smart money accumulation/distribution if wallet tags are available",
            "Compare extra pools against primary pool to ignore dust liquidity ghosts",
        ],
    }
