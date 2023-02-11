import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://postgres:postgres123@127.0.0.1:54320/techo'
    base_url: str = 'http://localhost:8000'
    local_env: bool = True

    class Config:
        env_file = os.getenv('ENV_FILE', 'dev.env')


@lru_cache()
def get_settings():
    return Settings()
