# =====================================================
# REDIS SPATIAL CACHE
# =====================================================

"""
Distributed spatial response cache.

Responsibilities:
- Redis connection management
- cache serialization
- TTL management
- cache lookup
- cache storage
"""

# =====================================================
# IMPORTS
# =====================================================

import json

from redis.asyncio import Redis

# =====================================================
# REDIS CONFIG
# =====================================================

REDIS_URL = "redis://127.0.0.1:6379"

# =====================================================
# REDIS CLIENT
# =====================================================

redis_client = Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)

# =====================================================
# CACHE TTL
# =====================================================

CACHE_TTL_SECONDS = 60 * 5

# =====================================================
# CACHE KEY
# =====================================================


def create_spatial_cache_key(
    resolution: int,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
):

    return (
        f"h3:"
        f"{resolution}:"
        f"{round(min_lon, 1)}:"
        f"{round(min_lat, 1)}:"
        f"{round(max_lon, 1)}:"
        f"{round(max_lat, 1)}"
    )


# =====================================================
# GET CACHE
# =====================================================


async def get_cache(key: str):

    cached = await redis_client.get(key)

    if cached:

        print("REDIS CACHE HIT")

        return json.loads(cached)

    print("REDIS CACHE MISS")

    return None


# =====================================================
# SET CACHE
# =====================================================


async def set_cache(
    key: str,
    value,
):

    await redis_client.set(
        key,
        json.dumps(value),
        ex=CACHE_TTL_SECONDS,
    )

    print("REDIS CACHE SET")
