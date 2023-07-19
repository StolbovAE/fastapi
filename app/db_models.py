import logging
from fastapi import status

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
            message = MessageResponse.from_orm(self)  # TODO: replace deprecated method
            response = PayloadResponse(payload=message)
        except Exception as error:
            logging.error(error)
            response = PayloadResponse(status_code=status.HTTP_404_NOT_FOUND, error="Message not found")
        return response

    def __repr__(self):
        return f"message: {self.id}"
