# Generated by Django 4.2.2 on 2023-07-16 08:28

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_message_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
