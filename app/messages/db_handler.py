import logging

from fastapi import status
from sqlalchemy.exc import IntegrityError

from app.base import async_session
from app.db_models import Message
from app.messages.models import CreateMessageRequest
from app.validators.response_validators import PayloadResponse


class MessageDbTable:
    async def create(self, new_msg: CreateMessageRequest) -> PayloadResponse:
        logging.debug(f"Started recording new message with params: {new_msg}")
        async with async_session() as session:
            new_message = Message(**new_msg.model_dump(exclude_none=True))
            try:
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)

                logging.debug(f'recorded in DB: {new_message.response}')

                return new_message.response

            except IntegrityError as error:
                await session.rollback()
                logging.warning(error)
                return PayloadResponse(status_code=status.HTTP_409_CONFLICT, error="already exist")
            except Exception as error:
                await session.rollback()
                logging.critical(error)
                return PayloadResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=error.args[0])
