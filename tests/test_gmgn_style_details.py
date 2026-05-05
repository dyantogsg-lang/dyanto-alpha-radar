from dyanto_alpha_radar.enrichment import build_gmgn_style_details


def test_build_gmgn_style_details_includes_security_pool_smart_money_and_timeframes():
    pair = {
        "liquidity_usd": 12000,
        "volume_24h": 360000,
        "volume_6h": 120000,
        "volume_1h": 25000,
        "volume_5m": 2200,
        "txns_24h_buys": 440,
        "txns_24h_sells": 610,
        "txns_1h_buys": 45,
        "txns_1h_sells": 25,
        "price_change_5m": 2.5,
        "price_change_1h": 18,
        "price_change_6h": 42,
        "price_change_24h": 190,
        "fdv": 280000,
        "pair_created_at": 1710000000000,
        "dex": "raydium",
        "pair_address": "PAIR",
        "url": "https://dexscreener.com/solana/PAIR",
        "raw": {"labels": ["pumpfun"], "boosts": {"active": 2}},
    }
    score = {"risk_score": 78, "opportunity_score": 66, "vol_liq": 30, "buy_ratio": 0.419}

    details = build_gmgn_style_details(pair, score, pair_count=4, social_score=25)

    assert "security" in details
    assert "pool" in details
    assert "smart_money" in details
    assert "timeframes" in details
    assert "holder_snapshot" in details
    assert details["security"]["liquidity_status"] == "thin"
    assert details["security"]["sell_pressure"] == "elevated"
    assert details["pool"]["dex"] == "raydium"
    assert details["timeframes"]["h24"]["volume_usd"] == 360000
    assert details["smart_money"]["signal"] in {"weak", "neutral", "watch"}
    assert any("first 70 buyers" in item.lower() for item in details["research_checklist"])
