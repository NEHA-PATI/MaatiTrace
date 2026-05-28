# =====================================================
# FASTAPI APPLICATION
# =====================================================

from fastapi import FastAPI
from core.config.settings import get_settings

from fastapi.middleware.cors import (
    CORSMiddleware,
)

from fastapi.middleware.gzip import (
    GZipMiddleware,
)

from services.api_gateway.app.api.v1.main import (
    router as api_v1_router,
)

# =====================================================
# APPLICATION
# =====================================================

app = FastAPI(
    title="Agri Platform API",
    version="1.0.0",
)

settings = get_settings()

# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# GZIP COMPRESSION
# =====================================================

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

# =====================================================
# API V1 ROUTES
# =====================================================

app.include_router(
    api_v1_router,
    prefix=settings.api_v1_prefix,
)

# =====================================================
# ROOT
# =====================================================


@app.get("/")
async def root():

    return {"message": "Agri Platform Backend Running"}
