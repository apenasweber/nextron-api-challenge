from pydantic import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    
    class Config:
        env_prefix = 'DATABASE_'

settings = Settings()
