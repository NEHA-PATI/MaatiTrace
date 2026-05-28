from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session import get_db

from core.database.models.state import State
from core.database.models.district import District
from core.database.models.block import Block
from core.database.models.village import Village

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()


# =====================================================
# GET STATES
# =====================================================


@router.get("/states")
async def get_states(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(State))

    states = result.scalars().all()

    return states


# =====================================================
# GET DISTRICTS
# =====================================================


@router.get("/districts/{state_id}")
async def get_districts(
    state_id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(District).where(District.state_id == state_id))

    districts = result.scalars().all()

    return districts


# =====================================================
# GET BLOCKS
# =====================================================


@router.get("/blocks/{district_id}")
async def get_blocks(
    district_id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(Block).where(Block.district_id == district_id))

    blocks = result.scalars().all()

    return blocks


# =====================================================
# GET VILLAGES
# =====================================================


@router.get("/villages/{block_id}")
async def get_villages(
    block_id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(Village).where(Village.block_id == block_id))

    villages = result.scalars().all()

    return villages
