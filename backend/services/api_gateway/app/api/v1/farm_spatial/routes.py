from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session import get_db

from core.database.models.farm import Farm
from core.database.models.farm_boundary import FarmBoundary

from core.database.models.farm_h3_cell import FarmH3Cell

from services.api_gateway.app.services.farm_spatial_service import (
    FarmSpatialService,
)

from services.api_gateway.app.api.v1.farm_spatial.schemas import (
    FarmSpatialResponse,
    FarmH3CellResponse,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()


# =====================================================
# GENERATE FARM H3 COVERAGE
# =====================================================


@router.post(
    "/{farm_id}/generate",
)
async def generate_farm_spatial(
    farm_id: int,
    db: AsyncSession = Depends(get_db),
):

    # =============================================
    # LOAD FARM
    # =============================================

    farm_result = await db.execute(select(Farm).where(Farm.id == farm_id))

    farm = farm_result.scalar_one_or_none()

    if not farm:
        raise HTTPException(
            status_code=404,
            detail="Farm not found",
        )

    # =============================================
    # LOAD ACTIVE BOUNDARY
    # =============================================

    boundary_result = await db.execute(
        select(FarmBoundary).where(
            FarmBoundary.farm_id == farm_id,
            FarmBoundary.is_active == True,
        )
    )

    boundary = boundary_result.scalar_one_or_none()

    if not boundary:
        raise HTTPException(
            status_code=404,
            detail="Boundary not found",
        )

    # =============================================
    # GENERATE H3 COVERAGE
    # =============================================

    generated_count = await FarmSpatialService.generate_farm_h3_cells(
        db,
        farm,
        boundary,
    )

    await db.commit()

    return {
        "farm_id": farm_id,
        "generated_cells": generated_count,
    }


# =====================================================
# GET FARM H3 CELLS
# =====================================================


@router.get(
    "/{farm_id}",
    response_model=FarmSpatialResponse,
)
async def get_farm_spatial(
    farm_id: int,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(select(FarmH3Cell).where(FarmH3Cell.farm_id == farm_id))

    cells = result.scalars().all()

    return FarmSpatialResponse(
        farm_id=farm_id,
        total_cells=len(cells),
        cells=[
            FarmH3CellResponse(
                h3_index=cell.h3_index,
                resolution=cell.resolution,
                coverage_ratio=cell.coverage_ratio,
            )
            for cell in cells
        ],
    )
