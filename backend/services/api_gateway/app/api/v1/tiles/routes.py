# =====================================================
# VECTOR TILE API
# =====================================================

"""
Production-grade vector tile serving.

Features:
- MVT generation
- zoom-based H3 resolution selection
- Web Mercator transformation
- hierarchical rendering
- spatial tile serving
- GPU-ready vector tiles
"""

# =====================================================
# IMPORTS
# =====================================================

from fastapi import APIRouter
from fastapi.responses import Response

from sqlalchemy import create_engine
from sqlalchemy import text

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()

# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "postgresql://postgres:Mikaelson@127.0.0.1:5432/agri_platform"

engine = create_engine(DATABASE_URL)

# =====================================================
# VECTOR TILE ENDPOINT
# =====================================================


@router.get("/{z}/{x}/{y}.mvt")
def get_vector_tile(
    z: int,
    x: int,
    y: int,
):

    # =================================================
    # TILE REQUEST LOGGING
    # =================================================

    print(f"\nTILE REQUEST: z={z}, x={x}, y={y}")

    # =================================================
    # SQL QUERY
    # =================================================

    query = text("""

        -- ============================================
        -- TILE ENVELOPE
        -- ============================================

        WITH tile AS (

            SELECT

                ST_TileEnvelope(
                    :z,
                    :x,
                    :y
                ) AS geom
        ),

        -- ============================================
        -- DYNAMIC H3 RESOLUTION SELECTION
        -- ============================================

        resolution_filter AS (

            SELECT

                CASE

                    WHEN :z <= 6 THEN 6
                    WHEN :z <= 8 THEN 7
                    WHEN :z <= 10 THEN 8
                    WHEN :z <= 12 THEN 9
                    ELSE 10

                END AS target_resolution
        ),

        -- ============================================
        -- VECTOR TILE GEOMETRY
        -- ============================================

        mvtgeom AS (

            SELECT

                h3_index,

                resolution,

                ST_AsMVTGeom(

    geometry_3857,

    tile.geom,

    4096,

    64,

    true

) AS geom

            FROM
                h3_cells,
                tile,
                resolution_filter

            WHERE
                resolution =
                resolution_filter.target_resolution

            AND ST_Intersects(

    geometry_3857,

    tile.geom
)
        )

        -- ============================================
        -- FINAL VECTOR TILE
        -- ============================================

        SELECT ST_AsMVT(

            mvtgeom,

            'h3_cells',

            4096,

            'geom'

        )

        FROM mvtgeom;

    """)

    # =================================================
    # EXECUTE QUERY
    # =================================================

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "z": z,
                "x": x,
                "y": y,
            },
        )

        tile_data = result.scalar()

    # =================================================
    # DEBUG LOGGING
    # =================================================

    if tile_data and len(tile_data) > 0:

        print(f"VECTOR TILE GENERATED: " f"{len(tile_data)} bytes")

    else:

        print("EMPTY TILE")

    # =================================================
    # RESPONSE
    # =================================================

    return Response(
        content=tile_data,
        media_type=("application/vnd.mapbox-vector-tile"),
        headers={
            # =========================================
            # BROWSER TILE CACHE
            # =========================================
            "Cache-Control": "public, max-age=3600",
        },
    )
