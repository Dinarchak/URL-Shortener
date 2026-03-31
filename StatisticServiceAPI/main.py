# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from settings import config
from consumer import KafkaConsumerWorker
from database import engine, Base
from routes import router
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


    loop = asyncio.get_running_loop()

    consumer_worker = KafkaConsumerWorker(
        config={
            "bootstrap.servers": config.kafka.bootstrap_servers,
            "group.id": config.kafka.group_id,
            "auto.offset.reset": "earliest"
        },
        topic=config.kafka.topics,
        loop=loop
    )

    consumer_worker.start()

    print("Kafka consumer started")

    yield

    consumer_worker.stop()
    print("Kafka consumer stopped")


app = FastAPI(lifespan=lifespan)
app.include_router(router)