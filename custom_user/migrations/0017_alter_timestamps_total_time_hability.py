# Generated by Django 3.2.20 on 2024-10-05 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0016_auto_20241005_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timestamps',
            name='total_time_hability',
            field=models.IntegerField(blank=True),
        ),
    ]