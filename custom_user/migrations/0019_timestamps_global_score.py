# Generated by Django 3.2.20 on 2024-10-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0018_timestamps_eff_gp'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamps',
            name='global_score',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
