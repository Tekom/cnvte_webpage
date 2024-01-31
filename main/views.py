from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate, login, logout
from custom_user.models import userData

# Create your views here.
def home(request):
    return render(request, 'main/index.html')

def loginPage(request):
	context = {}
	if request.method == 'POST':
		username = request.POST.get('username').lower()
		password = request.POST.get('password')

		try:
			user = User.objects.get(username=username)
		except:
			pass

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
			
		else:
			pass

	return render(request, 'main/login_register.html', context)

def register(request):
    if request.method == 'POST':
        #print('asd')
        firstname = request.POST.get('username').lower()
        lastname = request.POST.get('apellidos').lower()
        email = request.POST.get('email')
        universidad = request.POST.get('universidades')
        password = request.POST.get('password')

        User = get_user_model()
        user = User.objects.create_user(email=email,
                                 		password=password)
        
        new_user = userData(user = user, 
                            user_firstname = firstname, 
                            user_lastname = lastname,
                            university = universidad, 
                            email = email, )
        
        new_user.save()

        return render(request, 'main/index.html')

    return render(request, 'main/register.html')
    
