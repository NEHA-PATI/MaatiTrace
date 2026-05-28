from sqlalchemy import delete
from sqlalchemy import insert

from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models.farm_h3_cell import FarmH3Cell

# =====================================================
# FARM H3 REPOSITORY
# =====================================================


class FarmH3Repository:

    @staticmethod
    async def delete_farm_h3_cells(
        db: AsyncSession,
        farm_id: int,
    ):

        await db.execute(delete(FarmH3Cell).where(FarmH3Cell.farm_id == farm_id))

    @staticmethod
    async def bulk_insert(
        db: AsyncSession,
        records: list[dict],
        chunk_size: int = 10_000,
    ):

        if not records:
            return

        for start in range(0, len(records), chunk_size):
            chunk = records[start : start + chunk_size]

            await db.execute(
                insert(FarmH3Cell),
                chunk,
            )
