from confluent_kafka import Producer, KafkaException
from settings import config
from schemas import SlugSchema
from exceptions import EventSendingError

producer = Producer({'bootstrap.servers': config.kafka.bootstrap_servers})


def send_slug_creation(data: SlugSchema):
    try:
        producer.produce(
            topic=config.kafka.topic
            value=data.model_dump_json().encode('utf-8')
        )

        producer.poll(0)
    except KafkaException as e:
        raise EventSendingError(str(e)) from e