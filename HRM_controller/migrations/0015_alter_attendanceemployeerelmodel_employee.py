# Generated by Django 3.2.9 on 2022-02-22 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0010_employeeinformationmodel_shift'),
        ('HRM_controller', '0014_alter_attendanceemployeerelmodel_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceemployeerelmodel',
            name='employee',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_relation', to='HRM_Admin.employeeinformationmodel'),
        ),
    ]
