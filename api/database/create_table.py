from asyncio import run

from api.models.expression import Base

from api.database.connection import engine

async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    run(create_database())
