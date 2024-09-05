import json
from kafka import KafkaConsumer, KafkaProducer

kafka_server = ["localhost:9092"]


topic = "vehiculos_datos1"

consumer = KafkaConsumer(
    bootstrap_servers=kafka_server,
    value_deserializer=json.loads,
    api_version = (2, 8, 1),
    auto_offset_reset="latest",
)

consumer.subscribe(topic)

while True:
    data = next(consumer)
    print(data)
    print(data.value)