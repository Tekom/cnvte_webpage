# Generated by Django 5.0.2 on 2024-02-12 00:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0008_userdata_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='university',
            name='leader',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL),
        ),
    ]
