from . import settings
import psycopg2

def connect_to_db():
    return psycopg2.connect(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        database=settings.db_name,
    )
