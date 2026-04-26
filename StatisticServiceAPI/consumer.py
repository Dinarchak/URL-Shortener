from exceptions import RedirecEventRecordingException, CreateEventRecordingException
from schemas import RedirectEventSchema, CreationEventSchema
from service import add_redirect_event, add_create_event
from confluent_kafka import Consumer
from settings import config
from typing import Any
import threading
import json
import asyncio
from settings import config

class KafkaConsumerWorker:

    def __init__(self, config_: dict, topics: list[str], loop: asyncio.AbstractEventLoop):
        self.consumer = Consumer(config_)
        self.topics = topics
        self._running = False
        self._thread = None
        self.loop = loop

    def start(self):
        self._running = True
        self.consumer.subscribe(self.topics)

        self._thread = threading.Thread(target=self._consume_loop, daemon=True)
        self._thread.start()

    def _consume_loop(self):
        while self._running:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            print(msg, msg.topic())

            if msg.error():
                print(msg.error())
                continue

            topic = msg.topic()

            event = json.loads(msg.value().decode("utf-8"))

            future = asyncio.run_coroutine_threadsafe(
                self.process_event(event, topic),
                self.loop
            )

            def callback(fut):
                try:
                    fut.result()
                    print("✅ process_event выполнен")
                except Exception as e:
                    print(f"❌ Ошибка в process_event: {e}", end='\n\n')

            future.add_done_callback(callback)

    async def process_event(self, event: Any, topic: str):
        if topic == config.kafka.redirect_topic:
            try:
                await add_redirect_event(RedirectEventSchema(**event))
            except RedirecEventRecordingException as e:
                print(f'Что-то пошло не так во время фиксации события\n{e}', end='\n\n')
        elif topic == config.kafka.creation_topic:
            try:
                await add_create_event(CreationEventSchema(**event))
            except CreateEventRecordingException as e:
                print(f'Что-то пошло не так во время фиксации события\n{e}', end='\n\n')

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        self.consumer.close()
