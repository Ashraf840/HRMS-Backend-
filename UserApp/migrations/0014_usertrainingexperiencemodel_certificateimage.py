# Generated by Django 3.2.9 on 2022-01-18 06:34

import UserApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0013_auto_20220118_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertrainingexperiencemodel',
            name='certificateImage',
            field=models.FileField(blank=True, upload_to=UserApp.models.certificate_file_name),
        ),
    ]
