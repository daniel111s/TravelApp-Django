# Generated by Django 5.0 on 2024-01-14 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TravelWebApp", "0014_alter_task_description_alter_travel_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="travel",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 21, 20, 18, 20, 654706, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="start_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 14, 20, 18, 20, 654512, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
