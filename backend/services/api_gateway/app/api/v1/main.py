from fastapi import APIRouter

from services.api_gateway.app.api.v1.health.routes import (
    router as health_router,
)

from services.api_gateway.app.api.v1.h3.routes import (
    router as h3_router,
)

from services.api_gateway.app.api.v1.tiles.routes import router as tiles_router

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
