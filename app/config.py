from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dev")

    MODE: Literal["TEST", "DEV", "PROD"]
    LOG_LVL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_NAME: str

    TEST_DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DATABASE_URL(self):
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.sqlite3"

    @property
    def TEST_DATABASE_URL(self):
        return f"sqlite+aiosqlite:///./{self.TEST_DB_NAME}.sqlite3"


settings = Settings()
