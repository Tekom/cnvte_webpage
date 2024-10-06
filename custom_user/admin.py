from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin

from .models import *

admin.site.register(User, BaseUserAdmin)
admin.site.register(userData)
admin.site.register(University)
admin.site.register(Team)
admin.site.register(Timestamps)
