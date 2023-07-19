import logging

from fastapi import APIRouter

from app import config
from app.utils import broker_producer, broker_consumer
from app.messages.db_handler import MessageDbTable
from app.messages.models import CreateMessageRequest
from app.validators.response_validators import PayloadResponse

messages = APIRouter()


@messages.get("/send_message/{message}", response_model=PayloadResponse)
async def send_message(message: str):
    async with broker_producer() as producer:
        await producer.send_and_wait(config.BROKER_TOPIC, value=message.encode())
    return PayloadResponse(payload={"message": "Sent successfully"})


@messages.on_event("startup")
async def startup_event():
    async with broker_consumer() as consumer:
        async for msg in consumer:
            received_message = msg.value.decode()
            logging.debug(f"Got message from broker: {received_message}")

            message_data = CreateMessageRequest(**received_message)

            response = MessageDbTable.create(message_data)
            logging.debug(f"Got response: {response}")