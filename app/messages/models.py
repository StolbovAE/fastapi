from pydantic_settings import BaseSettings


class CreateMessageRequest(BaseSettings):
    text: str


class MessageResponse(CreateMessageRequest):
    id: int = ...

    class Config:
        orm_mode = True
        from_attributes = True
