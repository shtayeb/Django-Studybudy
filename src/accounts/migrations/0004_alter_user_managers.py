# Generated by Django 4.2.2 on 2023-07-01 08:08

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
