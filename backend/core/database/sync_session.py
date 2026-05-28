from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config.settings import get_settings

settings = get_settings()

# =====================================================
# SYNC ENGINE
# =====================================================

sync_engine = create_engine(
    settings.database_url.replace("+asyncpg", ""),
    echo=False,
)

# =====================================================
# SYNC SESSION
# =====================================================

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False,
)
