# Generated by Django 4.2.2 on 2023-07-30 09:45

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
