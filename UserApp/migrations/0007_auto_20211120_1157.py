# Generated by Django 3.2.9 on 2021-11-20 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_auto_20211120_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='useracademicinfomodel',
            name='cgpa',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='useracademicinfomodel',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='useracademicinfomodel',
            name='major',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='useracademicinfomodel',
            name='year',
            field=models.DateField(null=True),
        ),
    ]
