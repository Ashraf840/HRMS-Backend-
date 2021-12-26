# Generated by Django 3.2.9 on 2021-12-26 06:24

import UserApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0003_alter_userdepartmentmodel_deptmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentsubmissionmodel',
            name='digitalSignature',
            field=models.ImageField(blank=True, upload_to=UserApp.models.image_file_name),
        ),
        migrations.AddField(
            model_name='documentsubmissionmodel',
            name='passportSizePhoto',
            field=models.ImageField(blank=True, upload_to=UserApp.models.image_file_name),
        ),
        migrations.AlterField(
            model_name='documentsubmissionmodel',
            name='graduationCertificate',
            field=models.FileField(blank=True, upload_to=UserApp.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='documentsubmissionmodel',
            name='hscCertificate',
            field=models.FileField(blank=True, upload_to=UserApp.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='documentsubmissionmodel',
            name='sscCertificate',
            field=models.FileField(blank=True, upload_to=UserApp.models.content_file_name),
        ),
        migrations.AlterField(
            model_name='documentsubmissionmodel',
            name='userPassportImage',
            field=models.ImageField(blank=True, upload_to=UserApp.models.image_file_name),
        ),
    ]
