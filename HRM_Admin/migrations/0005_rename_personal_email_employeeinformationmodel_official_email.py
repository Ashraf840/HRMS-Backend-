# Generated by Django 3.2.9 on 2022-02-14 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0004_rename_accountno_employeebankinfomodel_account_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeinformationmodel',
            old_name='personal_email',
            new_name='official_email',
        ),
    ]
