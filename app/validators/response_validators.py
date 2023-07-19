from pydantic_settings import BaseSettings
from fastapi import status


class PayloadResponse(BaseSettings):
    status_code: int = status.HTTP_200_OK
    error: str = ""
    payload: dict = {}



