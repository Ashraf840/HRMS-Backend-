# Generated by Django 3.2.9 on 2022-01-18 04:20

import UserApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0012_alter_userworkingexperiencemodel_quitdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='useracademicinfomodel',
            name='cgpaOutOf',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='usercertificationsmodel',
            name='certificateImage',
            field=models.FileField(blank=True, upload_to=UserApp.models.certificate_file_name),
        ),
    ]
