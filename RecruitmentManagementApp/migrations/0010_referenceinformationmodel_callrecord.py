# Generated by Django 3.2.9 on 2022-02-04 06:29

import RecruitmentManagementApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0009_rename_refverified_referenceinformationmodel_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceinformationmodel',
            name='callRecord',
            field=models.FileField(blank=True, null=True, upload_to=RecruitmentManagementApp.models.content_file_name),
        ),
    ]
