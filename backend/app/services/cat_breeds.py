import time
import httpx
from app.core.config import settings

# cache 15 min
_CACHE: dict[str, tuple[float, set[str]]] = {}
_TTL = 900.0

async def fetch_breeds() -> set[str]:
    now = time.time()
    cached = _CACHE.get("breeds")
    if cached and (now - cached[0]) < _TTL:
        return cached[1]

    headers = {"x-api-key": settings.THECATAPI_KEY} if settings.THECATAPI_KEY else {}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(settings.THECATAPI_BASE, headers=headers)
        r.raise_for_status()
        data = r.json()

    breeds = {item["name"] for item in data if "name" in item}
    _CACHE["breeds"] = (now, breeds)
    return breeds

async def validate_breed(breed: str) -> bool:
    try:
        breeds = await fetch_breeds()
        return breed in breeds
    except Exception:
        return False
