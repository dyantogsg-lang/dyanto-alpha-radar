from __future__ import annotations

from dataclasses import dataclass

from dyanto_alpha_radar.adapters.dexscreener import fetch_token_pairs, search_pairs
from dyanto_alpha_radar.enrichment import build_gmgn_style_details
from dyanto_alpha_radar.scoring import classify_verdict, score_market


@dataclass
class RadarConfig:
    preferred_chain: str = "solana"
    min_liquidity_usd: float = 1_000
    social_keywords: tuple[str, ...] = ("twitter", "x.com", "telegram", "website", "pump.fun")


def pick_primary_pair(pairs: list[dict], preferred_chain: str = "solana") -> dict | None:
    if not pairs:
        return None
    filtered = [p for p in pairs if p.get("chain") == preferred_chain] or pairs
    return sorted(filtered, key=lambda p: (p.get("liquidity_usd") or 0, p.get("volume_24h") or 0), reverse=True)[0]


def extract_narrative(pair: dict) -> list[str]:
    raw = pair.get("raw") or {}
    items: list[str] = []
    info = raw.get("info") or {}
    for website in info.get("websites") or []:
        label = website.get("label") or "Website"
        url = website.get("url") or ""
        if url:
            items.append(f"{label}: {url}")
    for social in info.get("socials") or []:
        kind = social.get("type") or "social"
        url = social.get("url") or ""
        if url:
            items.append(f"{kind}: {url}")
    if not items:
        items.append("No public social metadata found in primary DEX feed")
    return items


def action_ideas(score: dict, pair: dict) -> list[str]:
    label = score["label"]
    if label == "HOT":
        return [
            "Track 5m/1h buy pressure; avoid chasing if risk score rises above 70",
            "Wait for liquidity expansion or controlled pullback before high-conviction entry",
        ]
    if label == "WARM+":
        return [
            "Monitor pullback support and whether volume/liquidity stays healthy",
            "Escalate if new holders/social catalyst expands without seller dominance",
        ]
    if label in {"RISKY", "AVOID"}:
        return [
            "Treat as watch-only until liquidity, holder spread, and seller pressure improve",
            "Do not use live execution; only dry-run simulation recommended",
        ]
    return ["Keep on monitor list; wait for stronger liquidity, breadth, or narrative confirmation"]


async def analyze(target: str, config: RadarConfig | None = None) -> dict:
    config = config or RadarConfig()
    try:
        pairs = await fetch_token_pairs(target)
    except Exception:
        pairs = await search_pairs(target)
    if not pairs:
        pairs = await search_pairs(target)
    primary = pick_primary_pair(pairs, config.preferred_chain)
    if not primary:
        return {"error": "No DEX pair found", "target": target, "pairs": []}

    score = score_market(primary)
    narrative = extract_narrative(primary)
    social_score = 70 if narrative and "No public" not in narrative[0] else 25
    holder_risk = min(90, score["risk_score"] + (15 if primary.get("liquidity_usd", 0) < 15_000 else 0))
    verdict = classify_verdict(
        {
            "market_score": score,
            "social_score": social_score,
            "holder_risk": holder_risk,
            "early_wallet_cluster": score["vol_liq"] > 20,
        }
    )

    details = build_gmgn_style_details(primary, score, pair_count=len(pairs), social_score=social_score)

    return {
        "identity": {
            "name": primary.get("name"),
            "symbol": primary.get("symbol"),
            "chain": primary.get("chain"),
            "address": primary.get("token_address"),
        },
        "primary_pair": {
            "dex": primary.get("dex"),
            "pair_address": primary.get("pair_address"),
            "url": primary.get("url"),
            "created_at": primary.get("pair_created_at"),
        },
        "market": {
            "price_usd": primary.get("price_usd"),
            "liquidity_usd": primary.get("liquidity_usd"),
            "volume_24h": primary.get("volume_24h"),
            "volume_6h": primary.get("volume_6h"),
            "volume_1h": primary.get("volume_1h"),
            "volume_5m": primary.get("volume_5m"),
            "fdv": primary.get("fdv"),
            "txns_24h_buys": primary.get("txns_24h_buys"),
            "txns_24h_sells": primary.get("txns_24h_sells"),
            "txns_1h_buys": primary.get("txns_1h_buys"),
            "txns_1h_sells": primary.get("txns_1h_sells"),
            "price_change_5m": primary.get("price_change_5m"),
            "price_change_1h": primary.get("price_change_1h"),
            "price_change_6h": primary.get("price_change_6h"),
            "price_change_24h": primary.get("price_change_24h"),
        },
        "score": score,
        "details": details,
        "verdict": verdict,
        "narrative": narrative,
        "actions": action_ideas(score, primary),
        "pair_count": len(pairs),
    }
