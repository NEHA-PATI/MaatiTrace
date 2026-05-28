import asyncio
import asyncpg


async def main():

    print("CONNECTING...")

    conn = await asyncpg.connect(
        user="postgres",
        password="Mikaelson",
        database="agri_platform",
        host="127.0.0.1",
        port=5432,
        ssl=False,
    )

    version = await conn.fetchval("SELECT version();")

    print("\nCONNECTED SUCCESSFULLY:\n")
    print(version)

    await conn.close()


asyncio.run(main())
