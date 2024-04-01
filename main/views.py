from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponse
import time
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, storage

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

cred = credentials.Certificate("./usuarios-cnvte-firebase-adminsdk-2izgz-0d7768c5f4.json")
firebase = firebase_admin.initialize_app(cred, 
					 {
						 'databaseURL': 'https://usuarios-cnvte-default-rtdb.firebaseio.com/',
						 'storageBucket': 'usuarios-cnvte.appspot.com'
					 })

#database = firebase.database()
ref_user = db.reference('Usuarios')
ref_leader = db.reference('Leaders')
bucket = storage.bucket()

# Inicializa la aplicación de Firebase Admin
#firebase_admin.initialize_app(cred)

@login_required(login_url='/login/')
def dashboard(request):
	context = {}

	user_logged = userData.objects.get(user = request.user)
	context = user_logged.Serialize()

	return render(request, 'main/dashboard.html', context)

# @login_required
# def sse(request):
# 	def event_stream():
# 		while True:

# 			last_db_item = dict(database.child('datos_vehiculo').order_by_key().limit_to_last(1).get().val()) #obtener ultimo dato en la base de datos
# 			last_car_data = last_db_item[list(last_db_item.keys())[0]]
		   
# 			#Generar datos para enviar al cliente
# 			data = {'engine_velocity':last_car_data['engine_velocity']['value_x'],
# 					'car_velocity':last_car_data['car_velocity']['value_x'],
# 					'voltage':last_car_data['voltage']['value_x'],
# 					'current':last_car_data['current']['value_x'],
# 					'pwm':last_car_data['pwm']['value_x'],
# 					'imu':{
# 							'x':last_car_data['imu']['x']['value_x'],
# 							'y':last_car_data['imu']['y']['value_x'],
# 							'z':last_car_data['imu']['z']['value_x']
# 					},
# 					'tiempo':last_car_data['tiempo']
# 			}
			
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
	logout(request)
	return redirect('login')


def register(request):
	university_codes = {'Universidad Militar Nueva Granada': ['UMNGLOSPROS', 'UMNGLOSMAX'],
						'Universidad De Los Andes':['ANDES1'],
						'Universidad Nacional Sede Bogotá':['NACBOGSTE'],
						'Universidad Nacional Sede Medellin':['NACMEDHYD'],
						'Universidad Pontificia Bolivariana':['UPB23'],
						'Universidad Autonoma De Occidente':['UAO67'],
						'Institucion Universitaria Pascual Bravo':['ESCBRAV1', 'ESCBRAVPH'],
						'Universidad Pontificia Bolivariana Sede Monteria':['UPBMONT9'],
						'EAFIT':['KRATOS&'],
						'Universidad Tecnologica De Pereira':['ITPGO1'],
						'Escuela De Ingenieros Julio Garavito':['ESCINGJG$'],
						'Universidad De Antioquia':['UDEASQUALLO'],
						'Universidad Autonoma De Manizales':['UAMCONT'],
						'Universidad Tecnológica De Bolívar':['UTBESH42', 'UTBTHU$@']}
	
	university_teams = {'Universidad Militar Nueva Granada': 2,
						'Universidad De Los Andes': 1,
						'Universidad Nacional (Bogotá)': 1,
						'Universidad Nacional (Medellin)': 1,
						'Universidad Pontificia Bolivariana': 1,
						'Universidad Autonoma De Occidente': 1,
						'Universidad Pontificia Bolivariana Sede Monteria':1,
						'Institucion Universitaria Pascual Bravo': 2,
						'EAFIT':1,
						'Universidad Tecnologica De Pereira':1,
						'Escuela De Ingenieros Julio Garavito':1,
						'Universidad De Antioquia':1,
						'Universidad Autonoma De Manizales':1,
						'Universidad Tecnológica De Bolívar':2}

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

	return render(request, 'main/register.html')
