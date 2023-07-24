# Generated by Django 4.2.2 on 2023-07-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_membership_is_blocked_room_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='blocked_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reaction',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='reactiontype',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='reactiontype',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]