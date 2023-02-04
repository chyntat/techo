import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://postgres:password@127.0.0.1:5432/new_db2'
    base_url: str = 'http://localhost:5432'
    local_env: bool = True

    # class Config:
    #     env_file = os.getenv('ENV_FILE', 'local.env')


@lru_cache()
def get_settings():
    return Settings()
