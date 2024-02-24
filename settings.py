from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL = 'sqlite:///db.sqlite3'
    SECRET_KEY = 'f8571e2edae9944931dfad979591bf5f0976666c7387dfce1a016b43bdeb3694'

def get_settings() -> Settings:
    return Settings()