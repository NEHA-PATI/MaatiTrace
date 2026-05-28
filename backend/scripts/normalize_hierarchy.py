import pandas as pd

from pathlib import Path

# =====================================================
# PATHS
# =====================================================

RAW_DIR = Path("data/farm_hierarchy/csv")

NORMALIZED_DIR = Path("data/farm_hierarchy/normalized")

NORMALIZED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =====================================================
# STORAGE
# =====================================================

states_list = []

districts_list = []

blocks_list = []

# =====================================================
# FILES
# =====================================================

csv_files = list(RAW_DIR.glob("*.csv"))

print(f"\nFOUND {len(csv_files)} CSV FILES\n")

# =====================================================
# PROCESS FILES
# =====================================================

for file in csv_files:

    print(f"\nPROCESSING: {file.name}")

    df = pd.read_csv(file)

    df.columns = df.columns.str.strip().str.lower()

    # =================================================
    # STATES
    # =================================================

    if "state lgd code" in df.columns:

        print("STATE FILE DETECTED")

        states_df = pd.DataFrame(
            {
                "state_code": (df["state lgd code"].astype(str).str.strip()),
                "state_name": (df["state name (in english)"].astype(str).str.strip()),
            }
        )

        states_list.append(states_df)

    # =================================================
    # DISTRICTS
    # =================================================

    elif "district lgd code" in df.columns:

        print("DISTRICT FILE DETECTED")

        districts_df = pd.DataFrame(
            {
                "district_code": (df["district lgd code"].astype(str).str.strip()),
                "district_name": (
                    df["district name (in english)"].astype(str).str.strip()
                ),
            }
        )

        districts_df["state_name"] = "Odisha"

        states_list.append(
            pd.DataFrame(
                {
                    "state_code": ["21"],
                    "state_name": ["Odisha"],
                }
            )
        )

        districts_list.append(districts_df)

    # =================================================
    # BLOCKS
    # =================================================

    elif "development block lgd code" in df.columns:

        print("BLOCK FILE DETECTED")

        blocks_df = pd.DataFrame(
            {
                "block_code": (
                    df["development block lgd code"].astype(str).str.strip()
                ),
                "block_name": (
                    df["development block name (in english)"].astype(str).str.strip()
                ),
            }
        )

        district_name = file.stem.replace("_block", "").strip()

        blocks_df["district_name"] = district_name

        blocks_list.append(blocks_df)

    else:

        print("UNKNOWN FILE TYPE")

# =====================================================
# CONCAT
# =====================================================

states_df = pd.concat(
    states_list,
    ignore_index=True,
).drop_duplicates()

districts_df = pd.concat(
    districts_list,
    ignore_index=True,
).drop_duplicates()

blocks_df = pd.concat(
    blocks_list,
    ignore_index=True,
).drop_duplicates()

# =====================================================
# EXPORT
# =====================================================

states_df.to_csv(
    NORMALIZED_DIR / "states.csv",
    index=False,
)

districts_df.to_csv(
    NORMALIZED_DIR / "districts.csv",
    index=False,
)

blocks_df.to_csv(
    NORMALIZED_DIR / "blocks.csv",
    index=False,
)

# =====================================================
# DONE
# =====================================================

print("\nNORMALIZATION COMPLETE")

print(f"\nSTATES: {len(states_df)}")

print(f"DISTRICTS: {len(districts_df)}")

print(f"BLOCKS: {len(blocks_df)}")
