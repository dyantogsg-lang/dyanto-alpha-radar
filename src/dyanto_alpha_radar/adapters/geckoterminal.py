from __future__ import annotations

import httpx

GECKO_BASE = "https://api.geckoterminal.com/api/v2"


def _float(value, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


async def fetch_pool(network: str, pool: str, timeout: float = 12.0) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{GECKO_BASE}/networks/{network}/pools/{pool}")
        response.raise_for_status()
        payload = response.json()
    data = payload.get("data") or {}
    attrs = data.get("attributes") or {}
    return {
        "source": "geckoterminal",
        "network": network,
        "pool": pool,
        "name": attrs.get("name") or "",
        "price_usd": _float(attrs.get("base_token_price_usd") or attrs.get("quote_token_price_usd")),
        "reserve_usd": _float(attrs.get("reserve_in_usd")),
        "volume_usd": attrs.get("volume_usd") or {},
        "transactions": attrs.get("transactions") or {},
        "raw": payload,
    }


async def fetch_token_price(network: str, token: str, timeout: float = 12.0) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{GECKO_BASE}/simple/networks/{network}/token_price/{token}")
        response.raise_for_status()
        payload = response.json()
    attrs = (payload.get("data") or {}).get("attributes") or {}
    return {"source": "geckoterminal", "network": network, "token": token, "prices": attrs.get("token_prices") or {}}
