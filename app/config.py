from pydantic import BaseSettings, root_validator

class Settings(BaseSettings):
    # DB_HOST:str
    # DB_PORT:int
    # DB_USER:str
    # DB_PASS:str
    # DB_NAME:str

    # @root_validator
    # def get_database_url(cls, v):
    #     v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
    #     return v


    # Все переменные необходимо хранить в файле .env,
    # но так как это пример, они останутся здесь, кроме
    # логина и пароля от почты
    # SMTP_HOST:str
    # SMTP_PORT:int
    # SMTP_USER:str
    # SMTP_PASS:str

    DATABASE_URL:str
    SYNC_DATABASE_URL = "sqlite:///./database.db"

    SECRET_KEY:str
    REFRESH_SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int
    APP_ORIGIN:str

    
    class Config:
        env_file = '.env'

settings = Settings()