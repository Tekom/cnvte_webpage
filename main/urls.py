from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('team_page/', views.teamPage, name='team_page'),
]


