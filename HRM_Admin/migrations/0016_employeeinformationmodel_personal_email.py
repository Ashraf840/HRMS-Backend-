# Generated by Django 3.2.9 on 2022-04-01 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0015_employeebankinfomodel_bank_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeinformationmodel',
            name='personal_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]