from fastapi import FastAPI

from app.api.v1.health.routes import router as health_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    application.include_router(health_router, prefix=settings.api_v1_prefix)
    return application


app = create_app()

