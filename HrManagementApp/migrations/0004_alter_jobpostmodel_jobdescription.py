# Generated by Django 3.2.9 on 2021-11-22 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HrManagementApp', '0003_auto_20211122_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpostmodel',
            name='jobDescription',
            field=models.TextField(null=True),
        ),
    ]
