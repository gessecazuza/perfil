# Generated by Django 4.2 on 2023-08-05 15:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("preference", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cookies",
            name="durationCookie",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 8, 12, 15, 36, 7, 501043, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
    ]
