# Generated by Django 5.0 on 2024-01-02 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("TravelWebApp", "0003_alter_travel_type_of_transport"),
    ]

    operations = [
        migrations.AlterField(
            model_name="travel",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 9, 11, 39, 5, 586798, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="travel",
            name="start_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 1, 2, 11, 39, 5, 586589, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
