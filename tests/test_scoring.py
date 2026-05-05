from dyanto_alpha_radar.scoring import score_market, classify_verdict


def test_score_market_rewards_liquidity_volume_and_buy_pressure():
    pair = {
        "liquidity_usd": 50000,
        "volume_24h": 500000,
        "txns_24h_buys": 1200,
        "txns_24h_sells": 800,
        "price_change_1h": 18,
        "price_change_24h": 75,
        "fdv": 400000,
    }

    result = score_market(pair)

    assert result["opportunity_score"] >= 70
    assert result["risk_score"] <= 55
    assert result["label"] in {"HOT", "WARM+"}


def test_score_market_flags_thin_liquidity_overheated_churn():
    pair = {
        "liquidity_usd": 7000,
        "volume_24h": 420000,
        "txns_24h_buys": 300,
        "txns_24h_sells": 700,
        "price_change_1h": -22,
        "price_change_24h": 240,
        "fdv": 90000,
    }

    result = score_market(pair)

    assert result["risk_score"] >= 75
    assert result["label"] in {"RISKY", "AVOID"}
    assert any("thin liquidity" in flag.lower() for flag in result["flags"])


def test_classify_verdict_uses_social_and_wallet_signals():
    verdict = classify_verdict({
        "market_score": {"opportunity_score": 78, "risk_score": 48},
        "social_score": 72,
        "holder_risk": 45,
        "early_wallet_cluster": True,
    })

    assert verdict == "Mixed"
