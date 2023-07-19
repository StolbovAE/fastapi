import logging
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app import config


@asynccontextmanager
async def broker_producer():
    try:
        producer = AIOKafkaProducer(bootstrap_servers=config.BROKER_SERVER)
        await producer.start()
        yield producer
    except Exception as error:
        logging.error(error)
        raise error

    await producer.stop()


@asynccontextmanager
async def broker_consumer():
    try:
        consumer = AIOKafkaConsumer(
                config.BROKER_TOPIC,
                bootstrap_servers=config.BROKER_SERVER,
                enable_auto_commit=False,
            )
        await consumer.start()
        yield consumer
    except Exception as error:
        logging.error(error)
        raise error

    await consumer.stop()