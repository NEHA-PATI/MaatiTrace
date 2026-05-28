import geopandas as gpd

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape

from core.database.models.state import State
from core.database.models.district import District

# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "postgresql+psycopg2://" "postgres:Mikaelson@127.0.0.1:5432/agri_platform"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# =====================================================
# MAIN
# =====================================================


def main():

    print("\nLOADING GEOJSON...\n")

    gdf = gpd.read_file(
        "data/boundaries/sambalpur.geojson",
        engine="pyogrio",
    )

    gdf = gdf.to_crs(epsg=4326)

    gdf = gdf.rename(
        columns={
            "district": "name",
        }
    )

    with Session(engine) as session:

        odisha = session.query(State).filter(State.name == "Odisha").first()

        if not odisha:

            print("ODISHA NOT FOUND")

            return

        for _, row in gdf.iterrows():

            district = (
                session.query(District).filter(District.name == row["name"]).first()
            )

            if district:

                district.geometry = from_shape(row["geometry"], srid=4326)

                print(f"UPDATED: {district.name}")

            else:

                district = District(
                    state_id=odisha.id,
                    name=row["name"],
                    geometry=from_shape(row["geometry"], srid=4326),
                )

                session.add(district)

                print(f"CREATED: {district.name}")

        session.commit()

    print("\nSAMBALPUR LOADED\n")


if __name__ == "__main__":
    main()
