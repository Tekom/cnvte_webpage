# Generated by Django 5.0.2 on 2024-02-26 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0011_alter_university_leader'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='members',
            new_name='members_team',
        ),
    ]