from __future__ import annotations

from datetime import datetime, timezone


def money(value) -> str:
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        value = 0
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:.4f}" if value < 1 else f"${value:.2f}"


def render_markdown_report(analysis: dict) -> str:
    identity = analysis.get("identity") or {}
    pair = analysis.get("primary_pair") or {}
    market = analysis.get("market") or {}
    score = analysis.get("score") or {}
    flags = score.get("flags") or []
    narrative = analysis.get("narrative") or []
    actions = analysis.get("actions") or []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# Dyanto AlphaRadar Report — {identity.get('symbol', 'UNKNOWN')}",
        "",
        f"Generated: {now}",
        "",
        "## What it is",
        f"- Name: {identity.get('name', 'Unknown')} ({identity.get('symbol', 'UNKNOWN')})",
        f"- Chain: {identity.get('chain', 'unknown')}",
        f"- Token: {identity.get('address', '')}",
        f"- Primary venue: {pair.get('dex', 'unknown')} / {pair.get('pair_address', '')}",
        f"- URL: {pair.get('url', '')}",
        "",
        "## Live structure",
        f"- Price: {money(market.get('price_usd'))}",
        f"- Liquidity: {money(market.get('liquidity_usd'))}",
        f"- 24h Volume: {money(market.get('volume_24h'))}",
        f"- FDV/Market Cap: {money(market.get('fdv'))}",
        f"- 24h Buys/Sells: {market.get('txns_24h_buys', 0)} / {market.get('txns_24h_sells', 0)}",
        f"- Price change 1h/24h: {market.get('price_change_1h', 0)}% / {market.get('price_change_24h', 0)}%",
        "",
        "## Score",
        f"- Label: {score.get('label', 'MONITOR')}",
        f"- Opportunity: {score.get('opportunity_score', 0)}/100",
        f"- Risk: {score.get('risk_score', 0)}/100",
        f"- Volume/Liquidity: {score.get('vol_liq', 0)}x",
        f"- Buy ratio: {score.get('buy_ratio', 0)}",
        "",
        "## Why it moved / narrative",
    ]
    lines.extend([f"- {item}" for item in narrative])
    lines.extend([
        "",
        "## Verdict",
        f"{analysis.get('verdict', 'Monitor')}",
        "",
        "## Risk flags",
    ])
    lines.extend([f"- {flag}" for flag in flags])
    lines.extend(["", "## Suggested actions"])
    lines.extend([f"- {action}" for action in actions])
    lines.extend([
        "",
        "## Safety mode",
        "Dry-run only by default. This project produces intelligence, not financial advice or automatic live execution.",
    ])
    return "\n".join(lines).strip() + "\n"
