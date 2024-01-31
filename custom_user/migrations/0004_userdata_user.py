# Generated by Django 3.2.20 on 2024-01-31 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_auto_20240131_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]