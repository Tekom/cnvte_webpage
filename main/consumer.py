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
    @sync_to_async
    def update_timestamp_record(self, timestamp, penalizacion):
        timestamp.total_penalization_hability = str(int(penalizacion))
        timestamp.save()

    @sync_to_async
    def update_eff(self, timestamp, efi):
        timestamp.eff_gp = str(float(efi))
        timestamp.save()

    @database_sync_to_async
    def get_sorted_teams_with_scores(self):
        # Obtenemos todos los registros del modelo `Timestamps`, ordenados por `total_time_hability`
        all_timestamps = Timestamps.objects.all().order_by('total_position_hability')
        valores = dict()

        for value in all_timestamps:
            valores[value.team.team] = int(value.total_position_hability) - int(value.total_penalization_hability)

        return valores
    
    @database_sync_to_async
    def get_sorted_teams_with_scores_acel(self):
        # Obtenemos todos los registros del modelo `Timestamps`, ordenados por `total_time_hability`
        all_timestamps = Timestamps.objects.all().order_by('total_position_acel')
        valores = dict()

        for value in all_timestamps:
            valores[value.team.team] = int(value.total_position_acel) - int(value.total_penalization_acel)

        return valores
    
    @database_sync_to_async
    def get_sorted_teams_with_global_scores(self):
        # Obtenemos todos los registros del modelo `Timestamps`, ordenados por `total_time_hability`
        all_timestamps = Timestamps.objects.all().order_by('global_score')
        valores = dict()

        for value in all_timestamps:
            valores[value.team.team] = value.global_score 

        return valores

    async def connect(self):
        self.cluster = Cluster(['cassandra_db'])
        self.session = self.cluster.connect('spark_streaming')

        await self.accept()

        user = self.scope["user"]
        cont = 0
                
        user_data = await sync_to_async(userData.objects.get)(user = user)
        user_team = user_data.team

        # team_object = await sync_to_async(Team.objects.get)(team = user_data.team)
        # team = await sync_to_async(Timestamps.objects.get)(team =  team_object)

        # get_module_logger(__name__).info(f'Team TS: {team}')

        while True:
            data = await self.get_data_from_cassandra(user_team)
            get_module_logger(__name__).info(f'Data WS: {data}')

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

        # get_module_logger(__name__).info(f'Data: {latest_record}')

        teams_results = dict()
        teams = await sync_to_async(list)(Team.objects.all())

        for team_data in teams:
            team_name = team_data.team
            team_timestamps = await sync_to_async(Timestamps.objects.get)(team = team_data)

            team_h_t1 = team_timestamps.time_stamp_1_hability
            team_h_t2 = team_timestamps.time_stamp_2_hability

            team_a_t1 = team_timestamps.time_stamp_1_acceleration
            team_a_t2 = team_timestamps.time_stamp_2_acceleration

            team_gp_t1 = team_timestamps.time_stamp_1_gp
            team_gp_t2 = team_timestamps.time_stamp_2_gp

            test_data = SimpleStatement(f"""
                SELECT car_voltage, car_current
                FROM spark_streaming.vehicules_data
                WHERE team_name = %s
                AND timestamp >= %s
                AND timestamp <= %s
            """)

            # get_module_logger(__name__).info(f'Data: {team_h_t1} - {team_h_t2}')

            hability_result = await sync_to_async(self.session.execute)(test_data, (team_name, team_h_t1, team_h_t2))
            acceleration_result = await sync_to_async(self.session.execute)(test_data, (team_name, team_a_t1, team_a_t2))
            grand_prix_result = await sync_to_async(self.session.execute)(test_data, (team_name, team_gp_t1, team_gp_t2))

            power = [(row.car_current * row.car_voltage)**2  for row in hability_result]
            power_gp = [(row.car_current * row.car_voltage)**2  for row in hability_result]

            filtered_powers = [num for num in power if (num ** 0.5) > 500]

            if len(filtered_powers) == 0:
                power = 0
                threshold = 0
            else:
                threshold = (len(filtered_powers) * 100) / (len(power))
                power = (sum(filtered_powers) / len(filtered_powers)) ** (0.5)

                # get_module_logger(__name__).info(f'Potencia RMS: {power}; Umbral: {threshold}')
                
            if len(power_gp) == 0:
                power_gp = 0
                consumo = 0
                efi=0
                
            else:
                power_gp = (sum(power_gp) / len(power)) ** (0.5)
                consumo = power_gp / (14 * 60)
                efi = 1/consumo

                await self.update_eff(team_timestamps, efi)

            if threshold > 10:
                penalizacion = power - 500
                await self.update_timestamp_record(team_timestamps, penalizacion)

            else:
                await self.update_timestamp_record(team_timestamps, 0)
                
            # teams_results[team_name] = power

        results = await self.get_sorted_teams_with_scores()
        results_acel = await self.get_sorted_teams_with_scores_acel()
        global_results = await self.get_sorted_teams_with_global_scores()

        sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        sorted_results_acel = dict(sorted(results_acel.items(), key=lambda item: item[1], reverse=True))
        sorted_global_results = dict(sorted(global_results.items(), key=lambda item: item[1], reverse=True))

        # get_module_logger(__name__).info(f'Data: {sorted_results}')

        if latest_record:
            return {
                'team_data': {
                                'id': latest_record.id,
                                'team_name': latest_record.team_name,
                                'car_velocity': int(latest_record.car_velocity),
                                'car_velocity_gps': int(latest_record.car_velocity_gps),
                                'car_voltage': int(latest_record.car_voltage),
                                'car_current': int(latest_record.car_current),
                                'power': int(latest_record.power),
                                'gps_1': float(latest_record.gps_1),
                                'gps_2': float(latest_record.gps_2),
                                'imu_x': float(latest_record.imu_x),
                                'imu_y': float(latest_record.imu_y),
                                'imu_z': float(latest_record.imu_z),
                                'timestamp': latest_record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                'average_velocity': round(float(average_data.average_velocity), 2),
                                'average_voltage': round(float(average_data.average_voltage), 2),
                                'average_current': round(float(average_data.average_current), 2),
                        }, 
                'teams_data': sorted_results,
                'teams_data_acel':sorted_results_acel,
                'global_scores': sorted_global_results 
            }
        
        else:
            return None
        
    