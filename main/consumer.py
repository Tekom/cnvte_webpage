from channels.generic.websocket import AsyncWebsocketConsumer

import json
from random import randint
from asyncio import sleep
from custom_user.models import *
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.cluster = Cluster(['casandra_db'])
        self.session = self.cluster.connect('spark_streaming')

        await self.accept()

        user = self.scope["user"]
        cont = 0
        
        user_data = await sync_to_async(userData.objects.get)(user = user)
        user_team = user_data.team

        

        for i in range(1000):
            data = await self.get_data_from_cassandra(user_team)

            await self.send(json.dumps(data))
            
            cont += 1
            await sleep(1)

    async def get_data_from_cassandra(self, team):
        query = SimpleStatement(f"SELECT * FROM spark_streaming.vehicules_data WHERE team_name = %s ORDER BY time_stamp DESC LIMIT 1 ALLOW FILT")  # Ajusta la consulta
        # Ejecutar la consulta de forma asíncrona
        result = await sync_to_async(self.session.execute)(query, (team,))
        
        # Procesar los resultados
        latest_record = result.one()

        if latest_record:
            return {
                    'id': latest_record.id,
                    'team_name': latest_record.team_name,
                    'car_velocity': latest_record.team_velocity,
                    'car_current': latest_record.car_current,
                    'gps': latest_record.gps
            }
        
        else:
            return None