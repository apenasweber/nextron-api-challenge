from typing import Optional
import psycopg2
import psycopg2.extras

from core import settings


def connect_to_db():
    return psycopg2.connect(
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        database=settings.db_name,
    )


class Database:
    def __init__(self):
        self.conn = None

    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()


def get_db() -> Database:
    return Database()
