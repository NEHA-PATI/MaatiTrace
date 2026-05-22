import geopandas as gpd

import h3

from shapely.geometry import Polygon

from sqlalchemy import create_engine
from sqlalchemy import text

DATABASE_URL = "postgresql://postgres:postgres" "@127.0.0.1:5433/agri_platform"

# ---------------------------------------------------
# DEVELOPMENT RESOLUTIONS
# ---------------------------------------------------

H3_RESOLUTIONS = [6, 7, 8, 9]


# ---------------------------------------------------
# H3 GENERATION
# ---------------------------------------------------


def polygon_to_h3_cells(
    geometry,
    resolution,
):

    geojson = geometry.__geo_interface__

    h3_indexes = h3.geo_to_cells(
        geojson,
        resolution,
    )

    return list(h3_indexes)


def h3_to_polygon(h3_index):

    boundary = h3.cell_to_boundary(h3_index)

    # h3 returns:
    # lat, lng
    #
    # shapely expects:
    # lng, lat

    coordinates = [(lng, lat) for lat, lng in boundary]

    return Polygon(coordinates)


# ---------------------------------------------------
# DATABASE HELPERS
# ---------------------------------------------------


def clear_existing_cells(engine):

    with engine.begin() as conn:

        conn.execute(text("""
                TRUNCATE h3_cells
                RESTART IDENTITY;
                """))


# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------


def main():

    engine = create_engine(DATABASE_URL)

    print("\nLoading district...\n")

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

    print("\nClearing old H3 cells...\n")

    clear_existing_cells(engine)

    rows = []

    for resolution in H3_RESOLUTIONS:

        print(f"\nGenerating H3 cells " f"for resolution {resolution}...\n")

        h3_indexes = polygon_to_h3_cells(
            district.geometry,
            resolution,
        )

        print(f"Generated " f"{len(h3_indexes)} cells")

        for h3_index in h3_indexes:

            polygon = h3_to_polygon(h3_index)

            rows.append(
                {
                    "h3_index": h3_index,
                    "resolution": resolution,
                    "district_id": district.id,
                    "geometry": polygon,
                }
            )

    print("\nCreating GeoDataFrame...\n")

    h3_gdf = gpd.GeoDataFrame(
        rows,
        geometry="geometry",
        crs="EPSG:4326",
    )

    print("\nPreview:\n")

    print(h3_gdf.head())

    print(f"\nTotal H3 cells: " f"{len(h3_gdf)}")

    print("\nUploading to PostGIS...\n")

    h3_gdf.to_postgis(
        name="h3_cells",
        con=engine,
        if_exists="append",
        index=False,
    )

    print("\nSUCCESSFULLY GENERATED " "MULTI-RESOLUTION H3 GRID\n")


if __name__ == "__main__":
    main()
