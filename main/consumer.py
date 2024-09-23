from channels.generic.websocket import AsyncWebsocketConsumer

import json
from random import randint
from asyncio import sleep
from custom_user.models import *
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
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

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.cluster = Cluster(['cassandra_db'])
        self.session = self.cluster.connect('spark_streaming')

        await self.accept()

        user = self.scope["user"]
        cont = 0
                
        user_data = await sync_to_async(userData.objects.get)(user = user)
        user_team = user_data.team

        for i in range(1000):
            data = await self.get_data_from_cassandra(user_team)

            if data is not None:
                data['y'] = cont

                await self.send(json.dumps(data))
                
                cont += 1
                await sleep(1)
            
            else:
                await sleep(1)

    async def get_data_from_cassandra(self, team):
        query = SimpleStatement(f"SELECT * FROM spark_streaming.vehicules_data WHERE team_name = %s ORDER BY timestamp DESC LIMIT 1")  # Ajusta la consulta

        averages = SimpleStatement(f"""
            SELECT AVG(car_velocity) as average_velocity, AVG(car_voltage) as average_voltage, AVG(car_current) as average_current
            FROM spark_streaming.vehicules_data
            WHERE team_name = %s
        """)

        # Ejecutar la consulta de forma asíncrona
        result = await sync_to_async(self.session.execute)(query, (team,))
        avg_query_result = await sync_to_async(self.session.execute)(averages, (team,))

        # Procesar los resultados
        latest_record = result.one()
        average_data = avg_query_result.one()

        get_module_logger(__name__).info(f'Data: {latest_record}')

        if latest_record:
            return {
                    'id': latest_record.id,
                    'team_name': latest_record.team_name,
                    'car_velocity': int(latest_record.car_velocity),
                    'car_voltage': int(latest_record.car_voltage),
                    'car_current': int(latest_record.car_current),
                    'gps_1': float(latest_record.gps_1),
                    'gps_2': float(latest_record.gps_2),
                    'timestamp': latest_record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'average_velocity': round(float(average_data.average_velocity), 2),
                    'average_voltage': round(float(average_data.average_voltage), 2),
                    'average_current': round(float(average_data.average_current), 2),
            }
        
        else:
            return None