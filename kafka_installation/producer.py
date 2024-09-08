import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import threading
import logging
from typing import List

def sendDataToTopic(topic):
    cont = 0

    get_module_logger(__name__).error(f'Started Thread for topic {topic}')
    get_module_logger(__name__).error(f'State for topic {topic}:{topic_state[topic]}')

    while topic_state[topic]:
                cont += 1
                data = {"eventId": f"{topic}", 
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
                
                get_module_logger(__name__).info(f'Data #{cont} Was Sent Succesfully')
                producer.send(topic_name_global, data)
                producer.flush()
                sleep(3)

    get_module_logger(__name__).error(f'State for topic {topic}:{topic_state[topic]}')

topic_2 = ['raptorrobotics', 
            'squalo-martello', 
            'kratos', 
            'elektron-motorsports', 
            'steos', 
            'formula-uam', 
            'e-force', 
            'pink-blinders', 
            'colombia-racing-team', 
            'unisabana-herons', 
            'hydrometra', 
            'barraquete', 
            'vteecci', 
            'senekart', 
            'e-shinott', 
            'furtivo-i', 
            'thundervolt', 
            'hamiltonev', 
            'miliracing', 
            'escuderia-bravo-N2', 
            'uao-firevolt']
    
# threads = [threading.Thread(target = sendDataToTopic, args = (topic_2[i],)) for i in range(len(topic_2))]

thread_state = [False] * len(topic_2)

# topics_threads = dict(zip(topic_2, threads))
topics_threads = dict()
topic_state = dict(zip(topic_2, thread_state))

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

get_module_logger(__name__).info(f'Threads {topics_threads}')
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
    
    except Exception as e:
        get_module_logger(__name__).error(f'Something went wrong while creating Kafka Admin due to {e}')
    
        return None
    
def Process(university_team: str = None):
    global producer, topic_name_global, topic_state

    producer = createKafkaProducer()
    topic_name_global = university_team

    if producer is not None:
        # create_topic = createKafkaTopic(topic_name = university_team)
        
        topic_state[university_team] = True

        topics_threads[university_team] = threading.Thread(target = sendDataToTopic, args = (university_team,))
        topics_threads[university_team].start()
            
def stopProcess(topic: str = None):
    topic_state[topic] = False


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