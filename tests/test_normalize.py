from dyanto_alpha_radar.adapters.dexscreener import normalize_pair


def test_normalize_dexscreener_pair_extracts_numeric_fields():
    raw = {
        "chainId": "solana",
        "dexId": "raydium",
        "pairAddress": "PAIR",
        "baseToken": {"address": "TOKEN", "name": "Token", "symbol": "TOK"},
        "priceUsd": "0.0025",
        "liquidity": {"usd": 12345.6},
        "volume": {"h24": 99999, "h1": 5000},
        "txns": {"h24": {"buys": 100, "sells": 40}},
        "priceChange": {"h1": 12.5, "h24": 80},
        "fdv": 250000,
        "url": "https://dexscreener.com/solana/PAIR",
    }

    pair = normalize_pair(raw)

    assert pair["chain"] == "solana"
    assert pair["symbol"] == "TOK"
    assert pair["price_usd"] == 0.0025
    assert pair["volume_24h"] == 99999.0
    assert pair["txns_24h_buys"] == 100
