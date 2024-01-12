# Generated by Django 4.2.7 on 2023-12-03 17:57

from django.db import migrations
import users.managers


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customuser",
            managers=[
                ("objects", users.managers.CustomUserManager()),
            ],
        ),
    ]