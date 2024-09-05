import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import threading
import logging

def get_module_logger(mod_name):
    """
    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger

def createKafkaProducer(): 
    """
    Kafka Producer for send vehicule's data to Spark Streaming
    """
    
    try:
        producer = KafkaProducer(
            bootstrap_servers="ed-kafka:29092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

        return producer
    
    except Exception as e:
        get_module_logger(__name__).error(f'Error creating KafkaProducer due to error: {e}')

        return None

def createAdminKafka():
    try:
        admin_client = KafkaAdminClient(
            bootstrap_servers="ed-kafka:29092"
        )

        return admin_client
    
    except:
        get_module_logger(__name__).error('Something went wrong while creating Kafka Admin')
    
        return None

def createKafkaTopic(topic_name: str = None) -> bool:
    kafka_admin = createAdminKafka()

    if kafka_admin is not None:
        if not topic_name in kafka_admin.list_topics():
            try:
                topic = NewTopic(
                    name = topic_name,
                    num_partitions = 5,  # Número de particiones
                    replication_factor = 1  # Factor de replicación
                )

                kafka_admin.create_topics(new_topics=[topic], validate_only=False)

                get_module_logger(__name__).info(f'Topic {topic_name} created succesfully')

                return True
            
            except Exception as e:
                get_module_logger(__name__).error(f'Unable to create Kafka topic due to error: {e}')

                return None
            
        else:   
            return True

# if __name__ == '__main__':

def sendDataToTopic():
    while True:
                data = {"eventId": "d0b8ce32-64e3-4e63-bd53-b0f7a2cb9b06", 
                        "eventOffset": 10045, 
                        "eventPublisher": "device", 
                        "customerId": "CI00103", 
                        "data": {
                            "devices": [
                                {"deviceId": "D003", 
                                "temperature": 20, 
                                "measure": "C", 
                                "status": "SUCCESS"}
                                ]
                            }, 
                        "eventTime": "2023-01-05 11:13:53.650313"}
                
                get_module_logger(__name__).info('Data Was Sent Succesfully')
                producer.send('device-data', data)
                producer.flush()
                sleep(3)

def Process(university_team: str = None):
    global producer
    producer = createKafkaProducer()

    if producer is not None:
        create_topic = createKafkaTopic(topic_name = university_team)

        if create_topic is not None:
            producer_thread = threading.Thread(target = sendDataToTopic)
            producer_thread.start()
            



# admin_client = KafkaAdminClient(
#     bootstrap_servers="localhost:9092",  # Reemplaza con la dirección de tu broker
# )
# admin_client.delete_topics(['test_topic'])

# Obtén la lista de temas
# topics = admin_client.list_topics()

# Muestra la lista de temas
# print("Lista de tópicos en Kafka:")
# for topic in topics:
#     print(topic)