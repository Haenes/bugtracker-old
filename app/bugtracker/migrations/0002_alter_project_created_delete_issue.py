# Generated by Django 4.2.1 on 2023-06-27 23:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 6, 27, 23, 19, 52, 893348, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
    ]
