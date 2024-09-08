from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import logging

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
    admin_client = KafkaAdminClient(
        bootstrap_servers="ed-kafka:29092"
    )

    for topic_name in topic_2:
        topic = NewTopic(
                    name = topic_name,
                    num_partitions = 5,  # Número de particiones
                    replication_factor = 1  # Factor de replicación
                )
        
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        get_module_logger(__name__).info(f'Topic {topic_name} created succesfully')

except Exception as e:
    get_module_logger(__name__).error(f'Something went wrong while creating Kafka Admin due to {e}')

