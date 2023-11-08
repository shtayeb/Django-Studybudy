# Generated by Django 4.2.2 on 2023-07-12 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0007_message_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                related_query_name="message",
                to="base.message",
            ),
        ),
    ]
