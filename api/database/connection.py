from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.retry_logic import create_engine_with_retry
from api.core.settings import settings

DATABASE_URL = settings.POSTGRES_URL

engine = engine = create_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
