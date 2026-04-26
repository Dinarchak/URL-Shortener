from confluent_kafka import Producer, KafkaException
from settings import config
from schemas import NewSlugSchemaEvent
from exceptions import EventSendingError

producer = Producer({'bootstrap.servers': config.kafka.bootstrap_servers})


def send_slug_creation(data: NewSlugSchemaEvent):
    try:
        producer.produce(
            topic=config.kafka.topic,
            value=data.model_dump_json().encode('utf-8')
        )

        print(data.model_dump_json())

        producer.poll(0)
    except KafkaException as e:
        raise EventSendingError(str(e)) from e