import asyncio

from dyanto_alpha_radar import analyzer


def test_analyze_includes_gmgn_style_details(monkeypatch):
    async def fake_fetch_token_pairs(target):
        return [
            {
                "chain": "solana",
                "dex": "raydium",
                "pair_address": "PAIR",
                "token_address": "TOKEN",
                "name": "Alpha",
                "symbol": "ALPHA",
                "price_usd": 0.001,
                "liquidity_usd": 20000,
                "volume_24h": 120000,
                "volume_6h": 30000,
                "volume_1h": 5000,
                "volume_5m": 200,
                "txns_24h_buys": 260,
                "txns_24h_sells": 180,
                "txns_1h_buys": 20,
                "txns_1h_sells": 12,
                "price_change_5m": 1,
                "price_change_1h": 5,
                "price_change_6h": 20,
                "price_change_24h": 80,
                "fdv": 160000,
                "url": "https://dexscreener.com/solana/PAIR",
                "raw": {"info": {"socials": [{"type": "twitter", "url": "https://x.com/a"}]}},
            }
        ]

    monkeypatch.setattr(analyzer, "fetch_token_pairs", fake_fetch_token_pairs)

    result = asyncio.run(analyzer.analyze("TOKEN"))

    assert result["details"]["pool"]["dex"] == "raydium"
    assert "security" in result["details"]
    assert "smart_money" in result["details"]
    assert result["market"]["volume_6h"] == 30000
