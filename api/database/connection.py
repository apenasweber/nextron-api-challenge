from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.core.settings import settings

DATABASE_URL = settings.POSTGRES_URL

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, class_=AsyncSession)

async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()