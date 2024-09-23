from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from cassandra.cluster import Cluster
import logging
import time

topics = ['raptorrobotics',
          'squalo martello',
          'kratos', 
          'elektron motorsports', 
          'steos', 
          'formula uam', 
          'e-force', 
          'pink blinders', 
          'colombia racing team', 
          'unisabana herons', 
          'hydrómetra', 
          'barraquete', 
          'vteecci', 
          'senekart', 
          'e-shinott', 
          'furtivo i', 
          'thundervolt', 
          'hamiltonev', 
          'miliracing', 
          'escuderia bravo N2', 
          'uao firevolt']

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

try:
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers="ed-kafka:29092"
            )

            break

        except:
            time.sleep(2)
            get_module_logger(__name__).info(f'Trying reconect to kafka cluster')

    for topic_name in topic_2:
        try:
            topic = NewTopic(
                        name = topic_name,
                        num_partitions = 5,  # Número de particiones
                        replication_factor = 1  # Factor de replicación
                    )
            
            admin_client.create_topics(new_topics=[topic], validate_only=False)
            get_module_logger(__name__).info(f'Topic {topic_name} created succesfully')

        except:
            get_module_logger(__name__).info(f'Topic {topic_name} alredy exist')
    
    try:
        while True:
            try:
                cluster = Cluster(['cassandra_db'])
                session = cluster.connect()

                break

            except:
                time.sleep(2)
                get_module_logger(__name__).info(f'Trying reconect to cassandra cluster')

        session.execute("""
                        CREATE KEYSPACE IF NOT EXISTS spark_streaming
                        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """)

        get_module_logger(__name__).info(f'Keyspace spark_streaming created succesfully')

    except Exception as e:
        get_module_logger(__name__).error(f'Failed to create keyspace spark_streaming due to error {e}')

    try:
        session.execute("""
                        CREATE TABLE IF NOT EXISTS spark_streaming.vehicules_data (
                            id TEXT,
                            team_name TEXT,
                            car_velocity FLOAT,
                            car_voltage FLOAT,
                            car_current FLOAT,
                            gps_1 FLOAT,
                            gps_2 FLOAT,
                            timestamp TIMESTAMP,
                            PRIMARY KEY (team_name, timestamp));
                """)
        
        get_module_logger(__name__).info(f'Table created successfully')

    except Exception as e:
        get_module_logger(__name__).error(f'Failed creating Table due to error {e}')

except Exception as e:
    get_module_logger(__name__).error(f'Something went wrong while creating Kafka Admin due to {e}')
    raise
