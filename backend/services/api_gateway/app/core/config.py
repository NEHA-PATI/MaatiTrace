from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MaatiTrace API Gateway"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="API_GATEWAY_")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

