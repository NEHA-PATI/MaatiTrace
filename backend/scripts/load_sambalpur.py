import geopandas as gpd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres" "@127.0.0.1:5433/agri_platform"


def main():

    print("\nLoading GeoJSON...\n")

    gdf = gpd.read_file(
        "data/boundaries/sambalpur.geojson",
        engine="pyogrio",
    )

    print("\nORIGINAL DATA:\n")
    print(gdf.head())

    print("\nORIGINAL COLUMNS:\n")
    print(gdf.columns)

    # -------------------------------------------------
    # CRS NORMALIZATION
    # -------------------------------------------------

    print("\nConverting CRS to EPSG:4326...\n")

    gdf = gdf.to_crs(epsg=4326)

    # -------------------------------------------------
    # SCHEMA NORMALIZATION
    # -------------------------------------------------

    print("\nNormalizing schema...\n")

    # GeoJSON has:
    # district, geometry

    # Database expects:
    # name, state, geometry

    gdf = gdf.rename(columns={"district": "name"})

    gdf["state"] = "Odisha"

    # keep only DB columns
    gdf = gdf[
        [
            "name",
            "state",
            "geometry",
        ]
    ]

    print("\nFINAL DATA:\n")
    print(gdf.head())

    print("\nFINAL COLUMNS:\n")
    print(gdf.columns)

    # -------------------------------------------------
    # DATABASE LOAD
    # -------------------------------------------------

    print("\nCreating DB connection...\n")

    engine = create_engine(DATABASE_URL)

    print("\nUploading to PostGIS...\n")

    gdf.to_postgis(
        name="districts",
        con=engine,
        if_exists="append",
        index=False,
    )

    print("\nSUCCESSFULLY LOADED SAMBALPUR\n")


if __name__ == "__main__":
    main()
