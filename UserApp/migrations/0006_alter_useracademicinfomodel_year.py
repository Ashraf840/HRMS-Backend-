# Generated by Django 3.2.9 on 2021-11-28 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_alter_useracademicinfomodel_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useracademicinfomodel',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
