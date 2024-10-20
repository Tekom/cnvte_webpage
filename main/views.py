from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
import time
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage
from django.views.decorators.csrf import csrf_exempt
from kafka_installation.producer import Process, stopProcess
import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import logging
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from custom_user.models import *

# Create your views here.
# config = {
# 			'apiKey': "AIzaSyCXoxYJ14-8THiRHs3VAM7KYNKnLEqhkMk",
# 			'authDomain': "hamiltonhv-database.firebaseapp.com",
# 			'databaseURL': "https://hamiltonhv-database-default-rtdb.firebaseio.com",
# 			'projectId': "hamiltonhv-database",
# 			'storageBucket': "hamiltonhv-database.appspot.com",
# 			'messagingSenderId': "1048401158234",
# 			'appId': "1:1048401158234:web:69af507d7af92aff357863",
# 			'measurementId': "G-F0E516TF2X"
# 		}

# firebase = pyrebase.initialize_app(config)
# authme = firebase.auth()
# database = firebase.database()
# createKafkaTopic(teams_topics = list(Team.objects.all()))

try:
	cred = credentials.Certificate("./usuarios-cnvte-firebase-adminsdk-2izgz-338c2bdd79.json")
	firebase = firebase_admin.initialize_app(cred, 
						{
							'databaseURL': 'https://usuarios-cnvte-default-rtdb.firebaseio.com/',
							'storageBucket': 'usuarios-cnvte.appspot.com'
						})

	#database = firebase.database()
	ref_user = db.reference('Usuarios')
	ref_universidades = db.reference('Universidades')
	ref_universidades_max_teams = db.reference('Equipos Totales')
	ref_leader = db.reference('Leaders')
	bucket = storage.bucket()
except ValueError:
	pass

# db_started = False
# # createKafkaTopic(teams_topic = list(Team.objects.all()))
# while not db_started:
# 	if firebase_admin._apps:
# 		createKafkaTopic(teams_topic = list(Team.objects.all()))
# 		db_started = True

# Inicializa la aplicación de Firebase Admin
#firebase_admin.initialize_app(cred)

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

@login_required(login_url='/login/')
def dashboard(request):
	

	context = {}

	user_logged = userData.objects.get(user = request.user)
	all_teams = Team.objects.values_list('team', flat=True).distinct()
	team = user_logged.team
	context = user_logged.Serialize()

	context['all_teams'] = all_teams
	context['user_team'] = team

	# print(user_logged.team)
	Process(university_team = user_logged.team,
	 		team_member = user_logged.Serialize()['member_name'])
	
	return render(request, 'main/dashboard.html', context)

# @login_required
# def sse(request):
# 	def event_stream():
# 		while True:

# 			last_db_item = dict(database.child('datos_vehiculo').order_by_key().limit_to_last(1).get().val()) #obtener ultimo dato en la base de datos
# 			last_car_data = last_db_item[list(last_db_item.keys())[0]]
		   
# 			#Generar datos para enviar al cliente
			# data = {'engine_velocity':'test',
			# 		'car_velocity':'test',
			# 		'voltage':'test',
			# 		'current':'test',
			# 		'pwm':'test',
			# 		'imu_x':'asd',
			# 		'imu_y':'asd',
			# 		'imu_z':'asd',
			# 		'tiempo':'test'
			# 	}
						
# 			#Formato SSE: envía un evento "message" con los datos
# 			event = f"data:{json.dumps(data)}\n\n"
			
# 			yield event
# 			time.sleep(1)

# 	response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
# 	return response


@login_required(login_url='/login/')
def teamPage(request):
	context = {}

	#Get user university
	university = Team.objects.get(team = userData.objects.get(user = request.user).team) #University.objects.get(university_name = userData.objects.get(user = request.user).university)
	
	#Modificar-----
	context['team_members'] = userData.objects.filter(user__in = university.members_team.all()) #Get all users data from university team
	context['leader'] = userData.objects.get(user = university.leader)
	context['members_count'] = len(context['team_members']) 
	context['university'] = University.objects.get(university_name = userData.objects.get(user = request.user).university)
	context['member_name'] = userData.objects.get(user = request.user)
	context['team_name'] = userData.objects.get(user = request.user).team.title()

	if request.user == university.leader:
		context['is_leader'] = True

	else:
		context['is_leader'] = False

	#------------------
	user_logged = userData.objects.get(user = request.user)

	try:
		stopProcess(topic = user_logged.team,
					team_member=user_logged.Serialize()['member_name'])
	except:
		pass

	return render(request, 'main/dashboard-crm.html', context)

def Scoreboard(request):
	return render(request, 'main/scoreboard.html')

def deleteUser(request):
	data = json.loads(request.body)
	user_id = int(data['user'])

	User_model = get_user_model()
	user_email = userData.objects.get(id = user_id).email

	User_model.objects.get(email = user_email).delete()

	return render(request, 'main/dashboard-crm.html')

def loginPage(request):
	context = {}
	if request.method == 'POST':
		email = request.POST.get('email').lower()
		password = request.POST.get('password')

		try:
			User = get_user_model()
			user = User.objects.get(email=email)
		except:
			pass

		user = authenticate(request, email=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('team_page')

		else:
			pass

	return render(request, 'main/index.html', context)


def logoutUser(request):
	user_logged = userData.objects.get(user = request.user)

	try:
		stopProcess(topic = user_logged.team,
					team_member = user_logged.Serialize()['member_name'])
		
	except:
		pass
	
	logout(request)
	return redirect('login')

def getData(firebase_data):
	universitys = list(firebase_data.keys())
	codes = []

	for university in universitys:
		codes.append(list(firebase_data[university].values()))

	valores_totales = dict(zip(universitys, codes))
	
	return (valores_totales, universitys)

def register(request):
	university_codes, universidades = getData(ref_universidades.get()[list(ref_universidades.get().keys())[0]])
	university_teams = ref_universidades_max_teams.get()[list(ref_universidades_max_teams.get().keys())[0]]

	if request.method == 'POST':
		firstname = request.POST.get('username').lower()
		lastname = request.POST.get('apellidos').lower()
		email = request.POST.get('email').lower()
		universidad = request.POST.get('universidades')
		password = request.POST.get('password')
		codigo_universidad = request.POST.get('access_code')
		team_name = request.POST.get('team_name')

		try:
			carta = request.FILES['filename']

		except:
			pass

		#print(carta)

		if codigo_universidad in university_codes[universidad]:
			if University.objects.filter(university_name = universidad).exists() and University.objects.get(university_name = universidad).teams.count() == university_teams[universidad]:
				return render(request, 'main/register.html', {'code':'True'})
					
			else:
				#Create leader model
				User = get_user_model()
				user = User.objects.create_user(email=email,
												password=password)

				#Leader data
				new_user = userData(user=user,
									user_firstname=firstname,
									user_lastname=lastname,
									university=universidad,
									email=email,
									team = team_name.lower() )

				new_user.save()

				#Create university instance

				if University.objects.filter(university_name = universidad).exists():
					new_team = Team(leader = user,
									team = team_name.lower())
				
					new_team.save()
					new_team.members_team.add(user)
					#new_university.teams.add(new_team)

					university = University.objects.get(university_name = universidad)
					university.teams.add(new_team)
					university.members.add(user)
	
					university.save()

					data = {'email':email,
							'password':password,
							'team_name':team_name,
							'codigo_universidad':codigo_universidad,
							'firstname':firstname,
							'lastname':lastname,
							'universidad':universidad,				
					}

					try:
						ref_leader.push(data)

						blob = bucket.blob(carta.name)

						with carta.open() as file:
							blob.upload_from_file(file, content_type=carta.content_type)
					
					except:
						pass
					
				else:
					new_team = Team(leader = user,
									team = team_name.lower())
					
					new_team.save()
					new_team.members_team.add(user)
					
					new_university = University(university_name = universidad)
					new_university.save()
					
					new_university.members.add(user)
					new_university.teams.add(new_team)

					data = {'email':email,
							'password':password,
							'team_name':team_name,
							'codigo_universidad':codigo_universidad,
							'firstname':firstname,
							'lastname':lastname,
							'universidad':universidad,				
					}

					ref_leader.push(data)

					try:
						blob = bucket.blob(carta.name)
						print('enviado')

						with carta.open() as file:
							print('enviado')
							blob.upload_from_file(file, content_type=carta.content_type)
					except:
						pass

				return redirect('login')

		else:
			try:
				#print(Team.objects.all())
				#print(str(team_name.lower))
				Team.objects.get(team = team_name.lower())

			except Exception as e:
				return render(request, 'main/register.html', {'code':'3'})
			
			if not University.objects.filter(university_name = universidad).exists():
				return render(request, 'main/register.html', {'code':'False'})
			
			elif Team.objects.get(team = team_name.lower()).members_team.count() == 15:
				return render(request, 'main/register.html', {'code':'2'})
			
			elif Team.objects.get(team = team_name.lower()).members_team.count() == 15:
				return render(request, 'main/register.html', {'code':'2'})
			
			else:
				#Create member instance
				User = get_user_model()
				user = User.objects.create_user(email=email,
												password=password)

				new_user = userData(user=user,
									user_firstname=firstname,
									user_lastname=lastname,
									university=universidad,
									email=email, 
									team = team_name.lower() )

				new_user.save()

				#Add member to university team
				member_university = University.objects.filter(university_name = universidad)[0]
				member_university.members.add(user)

				member_university.save()

				member_team = Team.objects.get(team = team_name.lower())
				member_team.members_team.add(user)
				member_university.teams.add(member_team)

				data = {'email':email,
							'password':password,
							'team_name':team_name,
							'codigo_universidad':codigo_universidad,
							'firstname':firstname,
							'lastname':lastname,
							'universidad':universidad,				
					}

				ref_user.push(data)

				return redirect('login')

	return render(request, 'main/register.html', context={'universidades':universidades})

def getPosTeams(data, prueba:str):
	resultados_con_puntajes = []

	for i, team_actual in enumerate(data):
		# team_actual.global_score = 0

		puntaje = 160 - (10 * (i + 1))  # +1 porque enumerate empieza en 0

		resultados_con_puntajes.append({
			'team': team_actual.team.team,
			'puntaje': puntaje
    	})

		if prueba == 'habilidad':
			team_actual.total_position_hability = str(puntaje) 

		if prueba == 'aceleracion':
			team_actual.total_position_acel = str(puntaje)

		# team_actual.global_score += (puntaje - int(team_actual.total_penalization_hability)) 
		team_actual.save()

	return resultados_con_puntajes

def addGlobalScores():
	scores = Timestamps.objects.all()

	for team in scores:
		team.global_score = int(team.total_position_hability) + int(team.total_position_acel) - int(team.total_penalization_hability) - int(team.total_penalization_acel)

		get_module_logger(__name__).info(f'Data WSf: {team.global_score}')
		team.save()

	return Timestamps.objects.all().order_by('global_score')

def updatePos(request):
	all_teams_hability = Timestamps.objects.all().order_by('total_time_hability')
	all_teams_accel = Timestamps.objects.all().order_by('total_time_aceleration')

	habilidad = getPosTeams(all_teams_hability, prueba = 'habilidad')
	aceleracion = getPosTeams(all_teams_accel, prueba = 'aceleracion')

	global_score = addGlobalScores()

	datos_completos = {
		'Habilidad': habilidad,
		'Aceleracion': aceleracion
	}
# Asignar puntajes según la posición
	
	# test = Timestamps.objects.all().order_by('total_time_hability')[0].team.team
	
	return JsonResponse(datos_completos, json_dumps_params={'indent': 4})

def showAnalitycs(request):
	cluster = Cluster(['cassandra_db'])
	session = cluster.connect('spark_streaming')
	
	query = """
			SELECT car_velocity, car_velocity_gps, car_voltage, car_current, power
			FROM spark_streaming.vehicules_data
			WHERE team_name = %s
			ORDER BY timestamp ASC
	"""

	user_logged = userData.objects.get(user = request.user)
	context = user_logged.Serialize()

	team = user_logged.team
	context['user_team'] = team

	rows = session.execute(query, [team])

	y = []
	car_velocity = []
	car_velocity_gps = []
	car_voltage = []
	car_current = []
	power = []

	for index, row in enumerate(rows):
		y.append(index)
		car_velocity.append(row.car_velocity)
		car_velocity_gps.append(row.car_velocity_gps)
		car_voltage.append(row.car_voltage)
		car_current.append(row.car_current)
		power.append(row.power)

	context['y'] = y
	context['car_velocity'] = car_velocity
	context['car_velocity_gps'] = car_velocity_gps
	context['car_voltage'] = car_voltage
	context['car_current'] = car_current
	context['power'] = power

	user_logged = userData.objects.get(user = request.user)

	try:
		stopProcess(topic = user_logged.team,
					team_member=user_logged.Serialize()['member_name'])
	except:
		pass
	
	get_module_logger(__name__).info(f'Cassandra Data: {context}')
	return render(request, 'main/analitycs.html', context)