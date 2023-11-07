# Generated by Django 4.2.2 on 2023-07-19 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("base", "0009_alter_message_body"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="participants",
        ),
        migrations.AlterField(
            model_name="room",
            name="host",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="host",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="base.room"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="room",
            name="members",
            field=models.ManyToManyField(blank=True, through="base.Membership", to=settings.AUTH_USER_MODEL),
        ),
    ]
