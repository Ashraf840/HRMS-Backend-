# Generated by Django 3.2.9 on 2022-01-13 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminOperationApp', '0014_rename_meetinglocation_interviewtimeschedulemodel_interviewlocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewtimeschedulemodel',
            name='interviewDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='interviewtimeschedulemodel',
            name='interviewTime',
            field=models.TimeField(),
        ),
    ]
