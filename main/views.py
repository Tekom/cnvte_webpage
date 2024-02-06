from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_user.models import *

# Create your views here.


@login_required
def dashboard(request):
	print(request.user)
	return render(request, 'main/dashboard.html')


def teamPage(request):
	return render(request, 'main/dashboard-crm.html')


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

		if codigo_universidad == codigos[universidad]:
			try:
				print(University.objects.filter(university_name = universidad))[0]

			except:
				User = get_user_model()
				user = User.objects.create_user(email=email,
												password=password)

				new_user = userData(user=user,
									user_firstname=firstname,
									user_lastname=lastname,
									university=universidad,
									email=email, )

				new_user.save()

				new_university = University(leader = user,
											university_name = universidad,

				)

				new_university.members.add(user)
				new_university.save()

		else:
			User = get_user_model()
			user = User.objects.create_user(email=email,
											password=password)

			new_user = userData(user=user,
								user_firstname=firstname,
								user_lastname=lastname,
								university=universidad,
								email=email, )

			new_user.save()

			member_university = University.objects.filter(university_name = universidad)[0]
			member_university.members.add(user)

			member_university.save()

		# return redirect('login')

	return render(request, 'main/register.html')
