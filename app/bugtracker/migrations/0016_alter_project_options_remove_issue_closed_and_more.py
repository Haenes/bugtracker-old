# Generated by Django 4.2.2 on 2023-08-03 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0015_alter_project_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-starred', 'created']},
        ),
        migrations.RemoveField(
            model_name='issue',
            name='closed',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='timespent',
        ),
    ]
