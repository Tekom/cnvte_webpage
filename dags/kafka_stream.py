# import uuid
# from datetime import datetime
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# import json
# from kafka import KafkaProducer
# import time
# import logging
# import requests

# default_args = {
#     'owner': 'Felipe',
#     'retries': 5,
# }

# def get_data():
#     res = requests.get("https://randomuser.me/api/")
#     res = res.json()
#     res = res['results'][0]

#     return res

# def format_data(res):
#     data = {}
#     location = res['location']
#     data['id'] = uuid.uuid4()
#     data['first_name'] = res['name']['first']
#     data['last_name'] = res['name']['last']
#     data['gender'] = res['gender']
#     data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
#                       f"{location['city']}, {location['state']}, {location['country']}"
#     data['post_code'] = location['postcode']
#     data['email'] = res['email']
#     data['username'] = res['login']['username']
#     data['dob'] = res['dob']['date']
#     data['registered_date'] = res['registered']['date']
#     data['phone'] = res['phone']
#     data['picture'] = res['picture']['medium']

#     return data

# def stream_data():
#     producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
#     curr_time = time.time()

#     while True:
#         if time.time() > curr_time + 60: #1 minute
#             break
#         try:
#             res = get_data()
#             res = format_data(res)

#             producer.send('users_created', json.dumps(res).encode('utf-8'))
#         except Exception as e:
#             logging.error(f'An error occured: {e}')
#             continue

# with DAG('user_automation',
#          default_args=default_args,
#          start_date=datetime(2024, 6, 9),
#          schedule_interval='@daily',
#          catchup=False) as dag:

#     streaming_task = PythonOperator(
#         task_id='stream_data_from_api',
#         python_callable=stream_data,
#         dag = dag
#     )

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Felipe',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id = 'first_dag',
    default_args=default_args,
    description='My first dag',
    start_date=datetime(2024, 5, 10, 2),
    schedule_interval="@daily"
) as dag:
    
    t1 = BashOperator(
        task_id = 't1',
        bash_command = 'echo hello world'
    )

    


