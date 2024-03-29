# Generated by Django 5.0 on 2024-01-13 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TravelWebApp", "0010_alter_travel_end_date_alter_travel_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="travel",
            name="description",
            field=models.CharField(default="", max_length=1000),
        ),
        migrations.AlterField(
            model_name="travel",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 20, 10, 45, 41, 215654, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="start_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 13, 10, 45, 41, 215431, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
