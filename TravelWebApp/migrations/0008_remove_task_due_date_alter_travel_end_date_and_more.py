# Generated by Django 5.0 on 2024-01-11 20:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TravelWebApp", "0007_task_alter_travel_end_date_alter_travel_start_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="due_date",
        ),
        migrations.AlterField(
            model_name="travel",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 18, 20, 15, 2, 451927, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="start_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 11, 20, 15, 2, 451734, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]