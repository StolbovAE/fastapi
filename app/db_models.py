import logging

from fastapi import status
from fastapi import HTTPException
from sqlalchemy import Column, Integer, String

from app.base import Base
from app.messages.models import MessageResponse
from app.validators.response_validators import PayloadResponse


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer(), primary_key=True, index=True)
    text = Column(String())

    @property
    def response(self):
        try:
            message = MessageResponse.model_validate(self)
            logging.debug(f"Model from ORM: {message}")
            response = PayloadResponse(payload=message)
        except Exception as error:
            logging.error(error)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")
        return response

    def __repr__(self):
        return f"message: {self.id}"
