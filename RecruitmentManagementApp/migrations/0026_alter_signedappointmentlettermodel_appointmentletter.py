# Generated by Django 3.2.9 on 2022-03-02 05:31

import RecruitmentManagementApp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0025_signedappointmentlettermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signedappointmentlettermodel',
            name='appointmentLetter',
            field=models.FileField(upload_to=RecruitmentManagementApp.models.appointment_file_name, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
