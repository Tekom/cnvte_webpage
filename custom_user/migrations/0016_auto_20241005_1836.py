# Generated by Django 3.2.20 on 2024-10-05 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0015_timestamps'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamps',
            name='total_penalization_hability',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='timestamps',
            name='total_position_hability',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='timestamps',
            name='total_time_hability',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
