from pydantic import BaseModel
import os

class Settings(BaseModel):
    db_user: str
    db_password: str
    db_host: str
    db_name: str


settings = Settings(
    db_user='postgres',
    db_password='password',
    db_host='localhost',
    db_name='nextron'
)
