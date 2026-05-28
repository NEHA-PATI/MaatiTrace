from fastapi import APIRouter

from services.api_gateway.app.api.v1.health.routes import (
    router as health_router,
)

from services.api_gateway.app.api.v1.h3.routes import (
    router as h3_router,
)

from services.api_gateway.app.api.v1.tiles.routes import router as tiles_router

from services.api_gateway.app.api.v1.farm_hierarchy.routes import (
    router as farm_hierarchy_router,
)


from services.api_gateway.app.api.v1.farms.routes import (
    router as farms_router,
)


from services.api_gateway.app.api.v1.farm_spatial.routes import (
    router as farm_spatial_router,
)

router = APIRouter()

# ---------------------------------------------------
# HEALTH ROUTES
# ---------------------------------------------------

router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

# ---------------------------------------------------
# H3 ROUTES
# ---------------------------------------------------

router.include_router(
    h3_router,
    prefix="/h3",
    tags=["H3"],
)

# ---------------------------------------------------
# TILE ROUTES
# ---------------------------------------------------

router.include_router(
    tiles_router,
    prefix="/tiles",
    tags=["Tiles"],
)

# ---------------------------------------------------
# FARM HIERARCHY ROUTES
# ---------------------------------------------------

router.include_router(
    farm_hierarchy_router,
    prefix="/farm-hierarchy",
    tags=["Farm Hierarchy"],
)


router.include_router(
    farms_router,
    prefix="/farms",
    tags=["Farms"],
)


router.include_router(
    farm_spatial_router,
    prefix="/farm-spatial",
    tags=["Farm Spatial"],
)
