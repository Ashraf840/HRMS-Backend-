# Generated by Django 3.2.9 on 2022-01-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0011_alter_useracademicinfomodel_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userworkingexperiencemodel',
            name='quitDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
