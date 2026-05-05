from dyanto_alpha_radar.api import home


def test_home_dashboard_uses_blue_white_premium_theme():
    html = home()

    assert "Dyanto AlphaRadar" in html
    assert "#0052ff" in html
    assert "#ffffff" in html
    assert "radar-shell" in html
    assert "metric-card" in html
    assert "opportunity" in html.lower()
    assert "risk" in html.lower()
    assert "scan()" in html


def test_home_dashboard_has_result_parser_cards():
    html = home()

    assert "renderAnalysis" in html
    assert "score-grid" in html
    assert "verdict-pill" in html
    assert "narrative-list" in html
    assert "actions-list" in html
