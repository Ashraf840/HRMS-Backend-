# Generated by Django 3.2.9 on 2022-02-15 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0005_rename_personal_email_employeeinformationmodel_official_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeinformationmodel',
            name='official_email',
        ),
    ]
