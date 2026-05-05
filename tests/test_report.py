from dyanto_alpha_radar.report import render_markdown_report


def test_render_markdown_report_contains_required_sections():
    analysis = {
        "identity": {"name": "Test Alpha", "symbol": "ALPHA", "chain": "solana", "address": "So111"},
        "primary_pair": {"dex": "raydium", "url": "https://dexscreener.com/solana/pair"},
        "market": {"price_usd": 0.001, "liquidity_usd": 25000, "volume_24h": 180000, "fdv": 300000},
        "score": {"opportunity_score": 74, "risk_score": 52, "label": "WARM+", "flags": ["High volume/liquidity"]},
        "verdict": "Mixed",
        "narrative": ["Fresh meme rotation"],
        "actions": ["Watch pullback above VWAP"],
    }

    md = render_markdown_report(analysis)

    assert "Dyanto AlphaRadar" in md
    assert "What it is" in md
    assert "Live structure" in md
    assert "Verdict" in md
    assert "Risk flags" in md
    assert "ALPHA" in md
