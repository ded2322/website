from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_USER: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str

    LOG_LEVEL:str

    model_config = SettingsConfigDict(env_file=".env_non_dev")


settings = Settings()
