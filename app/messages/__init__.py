import logging

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from fastapi import APIRouter

from app import config
from app.messages.db_handler import MessageDbTable
from app.messages.models import CreateMessageRequest
from app.validators.response_validators import PayloadResponse

messages = APIRouter()


@messages.get("/send_message/{message}", response_model=PayloadResponse)
async def send_message(message: str):
    producer = AIOKafkaProducer(bootstrap_servers=config.BROKER_SERVER)
    await producer.start()
    await producer.send_and_wait(config.BROKER_TOPIC, value=message.encode())
    await producer.stop()
    return PayloadResponse(payload={"message": "Sent successfully"})


@messages.on_event("startup")
async def startup_event():
    consumer = AIOKafkaConsumer(
        config.BROKER_TOPIC,
        bootstrap_servers=config.BROKER_SERVER,
        enable_auto_commit=False,
    )

    await consumer.start()
    async for msg in consumer:
        received_message = msg.value.decode()
        logging.debug(f"Got message from broker: {received_message}")

        message_data = CreateMessageRequest(**received_message)

        response = MessageDbTable().create(message_data)
        logging.debug(f"Got response: {response}")
    await consumer.stop()




