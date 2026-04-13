from confluent_kafka import Producer, KafkaException
from settings import config
from schemas import RedirectInfo
from exceptions import EventSendingError

producer = Producer({'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS})


def send_link_click(data: RedirectInfo):
    try:
        producer.produce(
            topic=config.KAFKA_TOPIC,
            value=data.model_dump_json().encode('utf-8') # encode преобразует строку в двоичный код
        )

        producer.poll(0)
    except KafkaException as e:
        raise EventSendingError(str(e)) from e
