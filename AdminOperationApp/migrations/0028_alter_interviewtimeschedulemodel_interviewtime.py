# Generated by Django 3.2.9 on 2022-03-08 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminOperationApp', '0027_alter_interviewtimeschedulemodel_interviewtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewtimeschedulemodel',
            name='interviewTime',
            field=models.TimeField(),
        ),
    ]
