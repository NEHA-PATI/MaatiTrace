# =====================================================
# H3 SPATIAL API
# =====================================================

"""
Production-grade viewport spatial serving.

Responsibilities:
- viewport bbox querying
- dynamic geometry simplification
- Redis distributed caching
- GeoJSON feature generation
- spatial observability
- rendering optimization
"""

# =====================================================
# IMPORTS
# =====================================================

import time

from fastapi import APIRouter

from sqlalchemy import create_engine
from sqlalchemy import text

from services.api_gateway.app.cache.redis_cache import (
    create_spatial_cache_key,
    get_cache,
    set_cache,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()

# =====================================================
# DATABASE CONFIG
# =====================================================

DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5433/agri_platform"

engine = create_engine(DATABASE_URL)

# =====================================================
# H3 CELLS API
# =====================================================


@router.get("/cells")
async def get_h3_cells(
    resolution: int,
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
):

    # =================================================
    # GEOMETRY SIMPLIFICATION TOLERANCE
    # =================================================

    tolerance_map = {
        5: 0.01,
        6: 0.005,
        7: 0.001,
        8: 0.0005,
        9: 0.0001,
    }

    tolerance = tolerance_map.get(
        resolution,
        0.0001,
    )

    # =================================================
    # START TIMER
    # =================================================

    start_time = time.time()

    print("NEW H3 ROUTE LOADED")

    # =================================================
    # REDIS CACHE KEY
    # =================================================

    cache_key = create_spatial_cache_key(
        resolution,
        min_lon,
        min_lat,
        max_lon,
        max_lat,
    )

    # =================================================
    # REDIS CACHE LOOKUP
    # =================================================

    cached_response = await get_cache(cache_key)

    if cached_response:

        return cached_response

    # =================================================
    # SQL QUERY
    # =================================================

    query = text("""

        SELECT jsonb_build_object(

            'type', 'FeatureCollection',

            'metadata', jsonb_build_object(

                'resolution', :resolution,

                'tolerance', :tolerance,

                'bbox', jsonb_build_object(
                    'min_lon', :min_lon,
                    'min_lat', :min_lat,
                    'max_lon', :max_lon,
                    'max_lat', :max_lat
                ),

                'feature_count', COUNT(*)

            ),

            'features',

            COALESCE(
                jsonb_agg(feature),
                '[]'::jsonb
            )

        )

        FROM (

            SELECT jsonb_build_object(

                'type', 'Feature',

                'geometry',

                ST_AsGeoJSON(

                    ST_SimplifyPreserveTopology(
                        geometry,
                        :tolerance
                    ),

                    5

                )::jsonb,

                'properties',

                jsonb_build_object(

                    'h3_index', h3_index,

                    'resolution', resolution

                )

            ) AS feature

            FROM h3_cells

            WHERE resolution = :resolution

            AND ST_Intersects(

                geometry,

                ST_MakeEnvelope(

                    :min_lon,
                    :min_lat,
                    :max_lon,
                    :max_lat,

                    4326

                )

            )

        ) features;

    """)

    # =================================================
    # EXECUTE QUERY
    # =================================================

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "resolution": resolution,
                "tolerance": tolerance,
                "min_lon": min_lon,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "max_lat": max_lat,
            },
        )

        geojson = result.scalar()

    # =================================================
    # QUERY METRICS
    # =================================================

    query_time_ms = round(
        (time.time() - start_time) * 1000,
        2,
    )

    # =================================================
    # ADD LATENCY METADATA
    # =================================================

    if geojson and "metadata" in geojson:

        geojson["metadata"]["query_time_ms"] = query_time_ms

    # =================================================
    # EMPTY SAFETY
    # =================================================

    if not geojson:

        return {
            "type": "FeatureCollection",
            "metadata": {
                "resolution": resolution,
                "tolerance": tolerance,
                "feature_count": 0,
                "query_time_ms": query_time_ms,
                "bbox": {
                    "min_lon": min_lon,
                    "min_lat": min_lat,
                    "max_lon": max_lon,
                    "max_lat": max_lat,
                },
            },
            "features": [],
        }

    # =================================================
    # STORE REDIS CACHE
    # =================================================

    await set_cache(
        cache_key,
        geojson,
    )

    # =================================================
    # RETURN GEOJSON
    # =================================================

    return geojson
