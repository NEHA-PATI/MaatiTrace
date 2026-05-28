import pandas as pd

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.database.models.state import State
from core.database.models.district import District
from core.database.models.block import Block

# =====================================================
# DATABASE
# =====================================================

DATABASE_URL = "postgresql+psycopg2://" "postgres:Mikaelson@127.0.0.1:5432/agri_platform"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)

# =====================================================
# FILES
# =====================================================

NORMALIZED_DIR = Path("data/farm_hierarchy/normalized")

states_df = pd.read_csv(NORMALIZED_DIR / "states.csv")

districts_df = pd.read_csv(NORMALIZED_DIR / "districts.csv")

blocks_df = pd.read_csv(NORMALIZED_DIR / "blocks.csv")

# =====================================================
# INGEST
# =====================================================

with Session(engine) as session:

    # =================================================
    # STATES
    # =================================================

    print("\nLOADING STATES...\n")

    for _, row in states_df.iterrows():

        exists = (
            session.query(State).filter(State.code == str(row["state_code"])).first()
        )

        if exists:
            continue

        state = State(
            name=row["state_name"],
            code=str(row["state_code"]),
        )

        session.add(state)

    session.commit()

    print("STATES LOADED")

    # =================================================
    # DISTRICTS
    # =================================================

    print("\nLOADING DISTRICTS...\n")

    for _, row in districts_df.iterrows():

        exists = (
            session.query(District)
            .filter(District.code == str(row["district_code"]))
            .first()
        )

        if exists:
            continue

        state = session.query(State).filter(State.name == row["state_name"]).first()

        if not state:
            continue

        district = District(
            state_id=state.id,
            name=row["district_name"],
            code=str(row["district_code"]),
            geometry=None,
        )

        session.add(district)

    session.commit()

    print("DISTRICTS LOADED")

    # =================================================
    # BLOCKS
    # =================================================

    print("\nLOADING BLOCKS...\n")

    for _, row in blocks_df.iterrows():

        exists = (
            session.query(Block).filter(Block.code == str(row["block_code"])).first()
        )

        if exists:
            continue

        district = (
            session.query(District)
            .filter(District.name == row["district_name"])
            .first()
        )

        if not district:
            continue

        block = Block(
            district_id=district.id,
            name=row["block_name"],
            code=str(row["block_code"]),
        )

        session.add(block)

    session.commit()

    print("BLOCKS LOADED")

print("\nHIERARCHY INGESTION COMPLETE\n")
