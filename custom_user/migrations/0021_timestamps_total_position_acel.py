# Generated by Django 3.2.20 on 2024-10-17 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0020_auto_20241017_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamps',
            name='total_position_acel',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]