# import geopandas as gpd

# import h3

# from shapely.geometry import Polygon

# from sqlalchemy import create_engine
# from sqlalchemy import text

# DATABASE_URL = "postgresql://postgres:Mikaelson" "@127.0.0.1:5432/agri_platform"

# # ---------------------------------------------------
# # DEVELOPMENT RESOLUTIONS
# # ---------------------------------------------------

# H3_RESOLUTIONS = [6, 7, 8, 9]


# # ---------------------------------------------------
# # H3 GENERATION
# # ---------------------------------------------------


# def polygon_to_h3_cells(
#     geometry,
#     resolution,
# ):

#     geojson = geometry.__geo_interface__

#     h3_indexes = h3.geo_to_cells(
#         geojson,
#         resolution,
#     )

#     return list(h3_indexes)


# def h3_to_polygon(h3_index):

#     boundary = h3.cell_to_boundary(h3_index)

#     # h3 returns:
#     # lat, lng
#     #
#     # shapely expects:
#     # lng, lat

#     coordinates = [(lng, lat) for lat, lng in boundary]

#     return Polygon(coordinates)


# # ---------------------------------------------------
# # DATABASE HELPERS
# # ---------------------------------------------------


# def clear_existing_cells(engine):

#     with engine.begin() as conn:

#         # =============================================
#         # CHECK IF TABLE EXISTS
#         # =============================================

#         result = conn.execute(text("""

#             SELECT EXISTS (

#                 SELECT FROM information_schema.tables

#                 WHERE table_name = 'h3_cells'

#             );

#         """))

#         table_exists = result.scalar()

#         # =============================================
#         # TRUNCATE ONLY IF EXISTS
#         # =============================================

#         if table_exists:

#             print("\nClearing old H3 cells...\n")

#             conn.execute(text("""

#                 TRUNCATE h3_cells
#                 RESTART IDENTITY;

#             """))

#         else:

#             print("\nh3_cells table does not exist yet.\n")


# # ---------------------------------------------------
# # MAIN PIPELINE
# # ---------------------------------------------------


# def main():

#     engine = create_engine(DATABASE_URL)

#     print("\nLoading district...\n")

#     district_gdf = gpd.read_postgis(
#         """
#         SELECT *
#         FROM districts
#         WHERE name = 'Sambalpur'
#         """,
#         con=engine,
#         geom_col="geometry",
#     )

#     district = district_gdf.iloc[0]

#     print("\nClearing old H3 cells...\n")

#     clear_existing_cells(engine)

#     rows = []

#     for resolution in H3_RESOLUTIONS:

#         print(f"\nGenerating H3 cells " f"for resolution {resolution}...\n")

#         h3_indexes = polygon_to_h3_cells(
#             district.geometry,
#             resolution,
#         )

#         print(f"Generated " f"{len(h3_indexes)} cells")

#         for h3_index in h3_indexes:

#             polygon = h3_to_polygon(h3_index)

#             rows.append(
#                 {
#                     "h3_index": h3_index,
#                     "resolution": resolution,
#                     "district_id": district.id,
#                     "geometry": polygon,
#                 }
#             )

#     print("\nCreating GeoDataFrame...\n")

#     h3_gdf = gpd.GeoDataFrame(
#         rows,
#         geometry="geometry",
#         crs="EPSG:4326",
#     )

#     print("\nPreview:\n")

#     print(h3_gdf.head())

#     print(f"\nTotal H3 cells: " f"{len(h3_gdf)}")

#     print("\nUploading to PostGIS...\n")

#     h3_gdf.to_postgis(
#         name="h3_cells",
#         con=engine,
#         if_exists="append",
#         index=False,
#     )

#     print("\nSUCCESSFULLY GENERATED " "MULTI-RESOLUTION H3 GRID\n")


# if __name__ == "__main__":
#     main()


import geopandas as gpd

import h3

from shapely.geometry import Polygon

from sqlalchemy import create_engine
from sqlalchemy import text

# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "postgresql+psycopg2://" "postgres:Mikaelson@127.0.0.1:5432/agri_platform"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# =====================================================
# RESOLUTIONS
# =====================================================

H3_RESOLUTIONS = [6, 7, 8, 9]

# =====================================================
# HELPERS
# =====================================================


def polygon_to_h3_cells(
    geometry,
    resolution,
):

    geojson = geometry.__geo_interface__

    cells = h3.geo_to_cells(
        geojson,
        resolution,
    )

    return list(cells)


def h3_to_polygon(h3_index):

    boundary = h3.cell_to_boundary(h3_index)

    coordinates = [(lng, lat) for lat, lng in boundary]

    return Polygon(coordinates)


# =====================================================
# MAIN
# =====================================================


def main():

    print("\nLOADING DISTRICT...\n")

    district_gdf = gpd.read_postgis(
        """
        SELECT *
        FROM districts
        WHERE name = 'Sambalpur'
        """,
        con=engine,
        geom_col="geometry",
    )

    district = district_gdf.iloc[0]

    with engine.begin() as conn:

        print("\nCLEARING OLD H3...\n")

        conn.execute(text("""
                TRUNCATE farm_h3_cells, h3_cells;
                """))

    rows = []

    for resolution in H3_RESOLUTIONS:

        print(f"\nGENERATING RESOLUTION {resolution}\n")

        h3_indexes = polygon_to_h3_cells(
            district.geometry,
            resolution,
        )

        print(f"GENERATED {len(h3_indexes)} CELLS")

        for h3_index in h3_indexes:

            polygon = h3_to_polygon(h3_index)

            rows.append(
                {
                    "h3_index": h3_index,
                    "resolution": resolution,
                    "geometry": polygon,
                }
            )

    h3_gdf = gpd.GeoDataFrame(
        rows,
        geometry="geometry",
        crs="EPSG:4326",
    )

    print(f"\nTOTAL CELLS: {len(h3_gdf)}")

    print("\nUPLOADING TO POSTGIS...\n")

    h3_gdf.to_postgis(
        "h3_cells",
        con=engine,
        if_exists="append",
        index=False,
    )

    with engine.begin() as conn:

        print("\nGENERATING 3857 GEOMETRY...\n")

        conn.execute(text("""
                UPDATE h3_cells
                SET geometry_3857 =
                ST_Transform(
                    geometry,
                    3857
                );
                """))

    print("\nH3 GENERATION COMPLETE\n")


if __name__ == "__main__":
    main()
