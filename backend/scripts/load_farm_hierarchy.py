import pandas as pd

from sqlalchemy import create_engine
from core.database.sync_session import (
    SyncSessionLocal,
)

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
# FILE PATHS
# =====================================================

STATES_CSV = "data/farm_hierarchy/normalized/states.csv"

DISTRICTS_CSV = "data/farm_hierarchy/normalized/districts.csv"

BLOCKS_CSV = "data/farm_hierarchy/normalized/blocks.csv"


# =====================================================
# LOAD DATAFRAMES
# =====================================================

states_df = pd.read_csv(STATES_CSV)

districts_df = pd.read_csv(DISTRICTS_CSV)

blocks_df = pd.read_csv(BLOCKS_CSV)


# =====================================================
# CLEAN DATA
# =====================================================

states_df = states_df.fillna("")
districts_df = districts_df.fillna("")
blocks_df = blocks_df.fillna("")


# =====================================================
# INGEST
# =====================================================

with SyncSessionLocal() as session:

    # =================================================
    # STATES
    # =================================================

    print("\nLOADING STATES...\n")

    for _, row in states_df.iterrows():

        state_code = str(row["state_code"]).strip()

        existing_state = session.query(State).filter(State.code == state_code).first()

        if existing_state:
            continue

        state = State(
            name=str(row["state_name"]).strip(),
            code=state_code,
        )

        session.add(state)

    session.commit()

    print("STATES LOADED")

    # =================================================
    # DISTRICTS
    # =================================================

    print("\nLOADING DISTRICTS...\n")

    for _, row in districts_df.iterrows():

        district_code = str(row["district_code"]).strip()

        existing_district = (
            session.query(District).filter(District.code == district_code).first()
        )

        if existing_district:
            continue

        # =============================================
        # FIND STATE
        # =============================================

        state = (
            session.query(State)
            .filter(State.name == str(row["state_name"]).strip())
            .first()
        )

        if not state:

            print(f"STATE NOT FOUND: " f"{row['state_name']}")

            continue

        district = District(
            state_id=state.id,
            name=str(row["district_name"]).strip(),
            code=district_code,
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

        block_code = str(row["block_code"]).strip()

        existing_block = session.query(Block).filter(Block.code == block_code).first()

        if existing_block:
            continue

        # =============================================
        # FIND DISTRICT
        # =============================================

        district = (
            session.query(District)
            .filter(District.name == str(row["district_name"]).strip())
            .first()
        )

        if not district:

            print(f"DISTRICT NOT FOUND: " f"{row['district_name']}")

            continue

        block = Block(
            district_id=district.id,
            name=str(row["block_name"]).strip(),
            code=block_code,
        )

        session.add(block)

    session.commit()

    print("BLOCKS LOADED")


# =====================================================
# DONE
# =====================================================

print("\nFARM HIERARCHY INGESTION COMPLETE\n")
