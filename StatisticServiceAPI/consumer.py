from exceptions import RedirecEventRecordingException
from schemas import RedirectEventSchema
from service import add_redirect_event
from confluent_kafka import Consumer
from settings import config
import threading
import json
import asyncio

class KafkaConsumerWorker:

    def __init__(self, config: dict, topic: str, loop: asyncio.AbstractEventLoop):
        self.consumer = Consumer(config)
        self.topic = topic
        self._running = False
        self._thread = None
        self.loop = loop

    def start(self):
        self._running = True
        self.consumer.subscribe([self.topic])

        self._thread = threading.Thread(target=self._consume_loop, daemon=True)
        self._thread.start()

    def _consume_loop(self):
        while self._running:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(msg.error())
                continue

            event = json.loads(msg.value().decode("utf-8"))

            future = asyncio.run_coroutine_threadsafe(
                self.process_event(RedirectEventSchema(**event)),
                self.loop
            )

            def callback(fut):
                try:
                    fut.result()
                    print("✅ process_event выполнен")
                except Exception as e:
                    print(f"❌ Ошибка в process_event: {e}")

            future.add_done_callback(callback)

            print(f'Новое сообщение: {event}')

    async def process_event(self, event: RedirectEventSchema):
        try:
            await add_redirect_event(event)
            print('добавил в бд')
        except RedirecEventRecordingException as e:
            print(f'Что-то пошло не так во время фиксации события\n{e}')

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        self.consumer.close()
