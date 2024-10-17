import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from datetime import datetime
import threading
import logging
from typing import List
from random import randint, uniform
from firebase_admin import credentials
from firebase_admin import db, storage
from random import randint, uniform
from datetime import datetime
import firebase_admin

certificates_path = {
    'hamiltonev': {
        'folder_name': 'hamilton',
        'certificate': 'hamiltondata-89832-firebase-adminsdk-ldp0m-ac90ac11da.json',
        'database':    'https://hamiltondata-89832-default-rtdb.firebaseio.com/'
    },
    'kratos': {
        'folder_name': 'kratos',
        'certificate': 'kratosdata-e957c-firebase-adminsdk-mdsa8-8e2c15c975.json',
        'database':    'https://kratosdata-e957c-default-rtdb.firebaseio.com/' 
    },
    'miliracing': {
        'folder_name': 'miliracing',
        'certificate': 'miliracingdata-firebase-adminsdk-6kc8c-9b0c461fc7.json',
        'database':    'https://miliracingdata-default-rtdb.firebaseio.com/'
    }
}

firebase_apps = dict()

def sendDataToTopic(topic):
    certificate_data = certificates_path[topic]
    
    if topic not in firebase_apps:
        try:
            cred = credentials.Certificate(f"./certificates/{certificate_data['folder_name']}/{certificate_data['certificate']}")
            firebase_apps[topic] =  firebase_admin.initialize_app(cred, 
                                                {
                                                    'databaseURL': certificate_data['database'],
                                                },
                                                name = topic)
        except ValueError:
            pass
    
    ref_user = db.reference('Data', firebase_apps[topic])
    cont = 0

    get_module_logger(__name__).info(f'Started Thread for topic {topic}')
    get_module_logger(__name__).info(f'State for topic {topic}:{topic_state[topic]}')

    while topic_state[topic]:
                # cont += 1
                # date = "_" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # timestamp = datetime.now()

                # data = {"id": f"{topic + date}",
                #         "team_name": f"{topic}", 
                #         "car_velocity": uniform(10.0, 40.0),
                #         "car_voltage": uniform(10.0, 40.0), 
                #         "car_current": uniform(10.0, 15.0),
                #         "gps_1": uniform(1.0, 1.001),
                #         "gps_2": uniform(1.0, 1.001), 
                #         "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                #     }
                
                # get_module_logger(__name__).info(f"Data sended: {data}")
                # get_module_logger(__name__).info(f'Data #{cont} Was Sent Succesfully')

                data = list(ref_user.order_by_key().limit_to_last(1).get().values())[0]
                # get_module_logger(__name__).error(f'Firebasedata {data}')
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
team_members = dict()

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

# get_module_logger(__name__).info(f'Threads {topics_threads}')

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
    
def Process(university_team: str = None, 
            team_member: str = None):
    
    global producer, topic_name_global, topic_state, team_members

    producer = createKafkaProducer()
    topic_name_global = university_team
    
    if university_team not in list(team_members.keys()):
         team_members[university_team] = []

    if team_member not in team_members[university_team]:
        team_members[university_team].append(team_member)

    if producer is not None:
        # create_topic = createKafkaTopic(topic_name = university_team)

        if not topic_state[university_team]:      
            topic_state[university_team] = True

            topics_threads[university_team] = threading.Thread(target = sendDataToTopic, args = (university_team,))
            topics_threads[university_team].start()

        else: return
            
def stopProcess(topic: str = None,
                team_member: str = None):
    
    team_members[topic].remove(team_member)
    get_module_logger(__name__).info(f"Amount of member remaining {team_members} from {topic}")

    if team_members[topic]:
         return
    
    else:
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