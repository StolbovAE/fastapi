import logging
from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE: str
    LOG_LEVEL: Union[int, str] = logging.INFO

    BROKER_SERVER: str
    BROKER_TOPIC: str

    class Config:
        env_file = ".env"
