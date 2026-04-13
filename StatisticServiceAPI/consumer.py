from exceptions import RedirecEventRecordingException
from schemas import RedirectEventSchema, CreationEventSchema
from service import add_redirect_event, add_create_event
from confluent_kafka import Consumer
from settings import config
from typing import Any
import threading
import json
import asyncio

class KafkaConsumerWorker:

    def __init__(self, config: dict, topics: list[str], loop: asyncio.AbstractEventLoop):
        self.consumer = Consumer(config)
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
            topic = msg.topic()

            if msg is None:
                continue

            if msg.error():
                print(msg.error())
                continue

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
        if topic == 'link-events':
            try:
                await add_redirect_event(RedirectEventSchema(**event))
            except RedirecEventRecordingException as e:
                print(f'Что-то пошло не так во время фиксации события\n{e}', end='\n\n')
        elif topic == 'slug-create-events':
            try:
                await add_create_event(CreationEventSchema(**event))
            except:
                print(f'Что-то пошло не так во время фиксации события\n{e}', end='\n\n')

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        self.consumer.close()
