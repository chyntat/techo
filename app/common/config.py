import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'sqlite:///./sql_app.db'  # TODO: change this appropriately
    base_url: str = 'http://localhost:8000'
    local_env: bool = True

    class Config:
        env_file = os.getenv('ENV_FILE', 'dev.env')


@lru_cache()
def get_settings():
    return Settings()
