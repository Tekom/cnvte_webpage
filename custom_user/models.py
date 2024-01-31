from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model


class User(BaseUser):
    objects = BaseUserManager()

class userData(models.Model):
    user_model = get_user_model()

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, default=None)
    user_firstname = models.CharField(max_length=200, blank=True)
    user_lastname = models.CharField(max_length=200, blank=True)
    university = models.CharField(max_length=200, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.user_firstname.capitalize() + ' ' + self.user_lastname.capitalize()
    

