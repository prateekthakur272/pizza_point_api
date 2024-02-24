from pydantic_settings import BaseSettings
from dotenv import dotenv_values


env_values = dotenv_values('.env')
class Settings(BaseSettings):
    DB_URL:str = 'sqlite:///db.sqlite3'
    SECRET_KEY:str = 'f8571e2edae9944931dfad979591bf5f0976666c7387dfce1a016b43bdeb3694'
    TOKEN_EXP_TIME:int = 60
    ALGORITHM:str = 'HS256'
    EMAIL:str = env_values['EMAIL']
    PASSWORD:str = env_values['PASSWORD']
    MAIL_SERVER:str = 'smtp.gmail.com'
    MAIL_SERVER_PORT:int = 465

def get_settings() -> Settings:
    return Settings()