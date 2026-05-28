import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:Mikaelson@127.0.0.1:5432/agri_platform"


async def test_connection():
    engine = create_async_engine(DATABASE_URL)

    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version();"))

        version = result.scalar()

        print("\nCONNECTED TO POSTGRESQL:\n")
        print(version)

    await engine.dispose()


asyncio.run(test_connection())
