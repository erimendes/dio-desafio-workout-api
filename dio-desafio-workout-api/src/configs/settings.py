from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Workout API"
    DATABASE_URL: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
