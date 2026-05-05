from __future__ import annotations

import httpx

DEX_BASE = "https://api.dexscreener.com/latest/dex"


def _float(value, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value, default: int = 0) -> int:
    return int(_float(value, default))


def normalize_pair(raw: dict) -> dict:
    base = raw.get("baseToken") or {}
    liquidity = raw.get("liquidity") or {}
    volume = raw.get("volume") or {}
    txns = raw.get("txns") or {}
    tx24 = txns.get("h24") or {}
    change = raw.get("priceChange") or {}
    return {
        "source": "dexscreener",
        "chain": raw.get("chainId") or "unknown",
        "dex": raw.get("dexId") or "unknown",
        "pair_address": raw.get("pairAddress") or "",
        "token_address": base.get("address") or "",
        "name": base.get("name") or "Unknown",
        "symbol": base.get("symbol") or "UNKNOWN",
        "price_usd": _float(raw.get("priceUsd")),
        "liquidity_usd": _float(liquidity.get("usd")),
        "volume_24h": _float(volume.get("h24")),
        "volume_6h": _float(volume.get("h6")),
        "volume_1h": _float(volume.get("h1")),
        "volume_5m": _float(volume.get("m5")),
        "txns_24h_buys": _int(tx24.get("buys")),
        "txns_24h_sells": _int(tx24.get("sells")),
        "txns_1h_buys": _int((txns.get("h1") or {}).get("buys")),
        "txns_1h_sells": _int((txns.get("h1") or {}).get("sells")),
        "price_change_5m": _float(change.get("m5")),
        "price_change_1h": _float(change.get("h1")),
        "price_change_6h": _float(change.get("h6")),
        "price_change_24h": _float(change.get("h24")),
        "fdv": _float(raw.get("fdv") or raw.get("marketCap")),
        "pair_created_at": raw.get("pairCreatedAt"),
        "url": raw.get("url") or "",
        "raw": raw,
    }


async def fetch_token_pairs(token: str, timeout: float = 12.0) -> list[dict]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{DEX_BASE}/tokens/{token}")
        response.raise_for_status()
        payload = response.json()
    return [normalize_pair(pair) for pair in payload.get("pairs") or []]


async def search_pairs(query: str, timeout: float = 12.0) -> list[dict]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{DEX_BASE}/search", params={"q": query})
        response.raise_for_status()
        payload = response.json()
    return [normalize_pair(pair) for pair in payload.get("pairs") or []]
