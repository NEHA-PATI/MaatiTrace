from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_env: str
    debug: bool

    api_v1_prefix: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    redis_host: str
    redis_port: int

    database_url: str

    secret_key: str

    r2_access_key: str | None = None
    r2_secret_key: str | None = None
    r2_bucket: str | None = None
    r2_endpoint: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
