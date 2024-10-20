from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model


class User(BaseUser):
    objects = BaseUserManager()

class Team(models.Model):
    user_model = get_user_model()

    leader = models.ForeignKey(user_model, on_delete=models.CASCADE, default=None, related_name='leader')
    members_team = models.ManyToManyField(user_model, related_name='team_members')
    team = models.CharField(max_length=200, blank = True)

    def __str__(self) -> str:
        return self.team.title()
    
class University(models.Model):
    user_model = get_user_model()

    university_name = models.CharField(max_length=100, blank=True)
    members = models.ManyToManyField(user_model, related_name='university_members')
    teams = models.ManyToManyField(Team, related_name='university_members')
    
    def __str__(self):
        return self.university_name.title()
    

class userData(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, default=None)
    user_firstname = models.CharField(max_length=200, blank=True)
    user_lastname = models.CharField(max_length=200, blank=True)
    university = models.CharField(max_length=200, blank=True)
    team = models.CharField(max_length=200, blank = True)
    email = models.EmailField()

    def __str__(self):
        return self.user_firstname.title() + ' ' + self.user_lastname.title()
    
    def Serialize(self):
        return {'member_name':self.user_firstname.capitalize() + ' ' + self.user_lastname.capitalize()}
    
class Timestamps(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    time_stamp_1_hability = models.CharField(max_length=200, blank=True)
    time_stamp_2_hability = models.CharField(max_length=200, blank=True)

    time_stamp_1_acceleration = models.CharField(max_length=200, blank=True)
    time_stamp_2_acceleration = models.CharField(max_length=200, blank=True)

    time_stamp_1_gp = models.CharField(max_length=200, blank=True)
    time_stamp_2_gp = models.CharField(max_length=200, blank=True)

    total_time_hability = models.IntegerField(blank=True)
    total_time_hability_2 = models.IntegerField(blank=True, default = 0)

    total_time_aceleration = models.IntegerField(blank=True, default = 0)
    total_time_aceleration_2 = models.IntegerField(blank=True, default = 0)

    total_penalization_hability = models.CharField(max_length=200, blank=True)
    total_penalization_acel = models.CharField(max_length=200, blank=True)

    total_position_hability = models.CharField(max_length=200, blank=True)
    total_position_acel = models.CharField(max_length=200, blank=True)

    global_score = models.IntegerField(default=0, blank=True)

    eff_gp =  models.FloatField(blank=True, default=0.0) 

    def __str__(self):
        return self.team.team.title() + " " + "Timestamps"