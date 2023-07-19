from pydantic_settings import BaseSettings


class PayloadResponse(BaseSettings):
    payload: dict = {}
