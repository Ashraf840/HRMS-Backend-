# Generated by Django 3.2.9 on 2021-12-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertrainingexperiencemodel',
            name='completeDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='usertrainingexperiencemodel',
            name='startDate',
            field=models.DateField(),
        ),
    ]
