# Generated by Django 4.2 on 2024-04-23 22:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preference', '0005_remove_preference_cidade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookies',
            name='durationCookie',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 30, 22, 9, 12, 685918, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]