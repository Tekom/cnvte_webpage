# Generated by Django 3.2.20 on 2024-01-31 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_userdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='university',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='userdata',
            name='user_firstname',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='userdata',
            name='user_lastname',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
