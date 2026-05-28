from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pyproj import Geod
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from shapely.geometry import Polygon

from geoalchemy2.shape import from_shape

from core.database.session import get_db

from core.database.models.farmer import Farmer
from core.database.models.farm import Farm
from core.database.models.farm_boundary import FarmBoundary

from services.api_gateway.app.api.v1.farms.schemas import (
    CreateFarmRequest,
)

from services.api_gateway.app.services.farm_spatial_service import (
    FarmSpatialService,
)

# =====================================================
# ROUTER
# =====================================================

router = APIRouter()

# =====================================================
# REGISTER FARM
# =====================================================


@router.post("/register")
async def register_farm(
    payload: CreateFarmRequest,
    db: AsyncSession = Depends(get_db),
):

    # =================================================
    # FIND OR CREATE FARMER
    # =================================================

    result = await db.execute(
        select(Farmer).where(Farmer.mobile_number == payload.mobile_number)
    )

    farmer = result.scalar_one_or_none()

    if not farmer:

        farmer = Farmer(
            full_name=payload.full_name,
            mobile_number=payload.mobile_number,
            aadhaar_reference=payload.aadhaar_reference,
            farmer_type=payload.farmer_type,
        )

        db.add(farmer)

        await db.flush()

    # =================================================
    # CREATE FARM
    # =================================================

    farm = Farm(
        farmer_id=farmer.id,
        block_id=payload.block_id,
        village_id=payload.village_id,
        village_name=payload.village_name,
        farm_name=payload.farm_name,
        ownership_type=payload.ownership_type,
        primary_crop=payload.primary_crop,
        irrigation_type=payload.irrigation_type,
        soil_type=payload.soil_type,
    )

    db.add(farm)

    await db.flush()

    # =================================================
    # BUILD POLYGON
    # =================================================

    polygon_coords = [(coord.lng, coord.lat) for coord in payload.boundary_coordinates]

    if len(polygon_coords) < 3:
        raise HTTPException(
            status_code=400,
            detail="Farm boundary requires at least 3 coordinates",
        )

    # close polygon automatically

    if polygon_coords[0] != polygon_coords[-1]:

        polygon_coords.append(polygon_coords[0])

    polygon = Polygon(polygon_coords)

    # =================================================
    # VALIDATION
    # =================================================

    if not polygon.is_valid:

        raise HTTPException(
            status_code=400,
            detail="Invalid polygon geometry",
        )

    # =================================================
    # AREA
    # =================================================

    geod = Geod(ellps="WGS84")

    area_m2, _ = geod.geometry_area_perimeter(polygon)

    area_m2 = abs(area_m2)

    # =================================================
    # BOUNDARY HASH
    # =================================================

    boundary_hash = hashlib.sha256(polygon.wkt.encode()).hexdigest()

    # =================================================
    # STORE BOUNDARY
    # =================================================

    boundary = FarmBoundary(
        farm_id=farm.id,
        boundary=from_shape(
            polygon,
            srid=4326,
        ),
        boundary_hash=str(hash(polygon.wkt)),
        version=1,
        area_m2=area_m2,
        is_active=True,
    )

    db.add(boundary)

    await FarmSpatialService.generate_farm_h3_cells(
        db,
        farm,
        boundary,
    )

    await db.commit()

    return {
        "message": "Farm registered successfully",
        "farm_id": farm.id,
        "boundary_id": boundary.id,
    }
