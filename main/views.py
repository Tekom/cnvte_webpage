from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponse
import time
import json
from custom_user.models import *

# Create your views here.


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
			return redirect('dashboard')

		else:
			pass

	return render(request, 'main/index.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def register(request):
	university_codes = {'Universidad Militar Nueva Granada': 'gkmlhf',
						'Universidad De Los Andes':'asdsad',
						'Universidad Nacional (Bogotá)':'szkjfhsa',
						'Universidad Nacional (Medellin)':'szkjfhsjhba',
						'Universidad Pontificia Bolivariana':'ksjajdfsadjk',
						'Universidad Autonoma De Occidente':'sakdjnsakjd',
						'Institucion Universitaria Pascual Bravo':'86sdf78',
						'EAFIT':'sajkcfnsajkc',
						'Institucion Universitaria Pascual Bravo':'86sdf78',
						'ITP':'86sdf78',
						'Escuela de ingenieros':'86sdf78',
						'UDEA':'86sdfdfg78'}
	
	university_teams = {'Universidad Militar Nueva Granada': 2,
						'Universidad De Los Andes': 1,
						'Universidad Nacional (Bogotá)': 1,
						'Universidad Pontificia Bolivariana': 2,
						'Universidad Autonoma De Occidente': 1,
						'Institucion Universitaria Pascual Bravo': 2,
						'EAFIT':1,
						'ITP':1,
						'Escuela de ingenieros':1,
						'UDEA':1}

	if request.method == 'POST':
		firstname = request.POST.get('username').lower()
		lastname = request.POST.get('apellidos').lower()
		email = request.POST.get('email').lower()
		universidad = request.POST.get('universidades')
		password = request.POST.get('password')
		codigo_universidad = request.POST.get('access_code')
		team_name = request.POST.get('team_name')

		if codigo_universidad == university_codes[universidad]:
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
					
				else:
					new_team = Team(leader = user,
									team = team_name.lower())
					
					new_team.save()
					new_team.members_team.add(user)
					
					new_university = University(university_name = universidad)
					new_university.save()
					
					new_university.members.add(user)
					new_university.teams.add(new_team)
				

				return redirect('login')

		else:
			if not University.objects.filter(university_name = universidad).exists():
				return render(request, 'main/register.html', {'code':'False'})
				
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

				return redirect('login')

	return render(request, 'main/register.html')
