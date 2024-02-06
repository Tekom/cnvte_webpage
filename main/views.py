from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_user.models import *

# Create your views here.


@login_required(login_url='/login/')
def dashboard(request):
	context = {}

	user_logged = userData.objects.get(user = request.user)
	
	context = user_logged.Serialize()

	return render(request, 'main/dashboard.html', context)


@login_required(login_url='/login/')
def teamPage(request):
	context = {}

	#Get user university
	university = University.objects.get(university_name = userData.objects.get(user = request.user).university)
	
	context['team_members'] = userData.objects.filter(user__in = university.members.all()) #Get all users data from university team
	context['leader'] = userData.objects.get(user = university.leader)
	context['members_count'] = len(context['team_members']) + 1
	context['university'] = university
	context['member_name'] = userData.objects.get(user = request.user)
	context['team_name'] = userData.objects.get(user = request.user).team

	print(context)

	return render(request, 'main/dashboard-crm.html', context)


def loginPage(request):
	context = {}
	if request.method == 'POST':
		email = request.POST.get('email').lower()
		password = request.POST.get('password')

		try:
			User = get_user_model
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
	codigos = {'Universidad Militar Nueva Granada': 'gkmlhf',
			   'Universidad Militar Nueva Granada': 'gkmlhf', }

	if request.method == 'POST':
		# print('asd')
		firstname = request.POST.get('username').lower()
		lastname = request.POST.get('apellidos').lower()
		email = request.POST.get('email')
		universidad = request.POST.get('universidades')
		password = request.POST.get('password')
		codigo_universidad = request.POST.get('access_code')
		team_name = request.POST.get('team_name')

		if codigo_universidad == codigos[universidad]:
			try:
				#Check if there is alredy a university instance
				print(University.objects.filter(university_name = universidad))[0]

			except:
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
									team_name = team_name )

				new_user.save()

				#Create university instance
				new_university = University(leader = user,
											university_name = universidad,

				)

				#new_university.members.add(user)
				new_university.save()

		else:
			#Create member instance
			User = get_user_model()
			user = User.objects.create_user(email=email,
											password=password)

			new_user = userData(user=user,
								user_firstname=firstname,
								user_lastname=lastname,
								university=universidad,
								email=email, )

			new_user.save()

			#Add member to university team
			member_university = University.objects.filter(university_name = universidad)[0]
			member_university.members.add(user)

			member_university.save()

		return redirect('login')

	return render(request, 'main/register.html')
