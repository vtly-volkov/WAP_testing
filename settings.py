from functools import lru_cache

from pydantic_settings import BaseSettings
from os import environ


class Settings(BaseSettings):
    TWITCH_URL: str
    WAIT_TIMEOUT: int

    class Config:
        env_file = environ.get("ENV_FILE", ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
