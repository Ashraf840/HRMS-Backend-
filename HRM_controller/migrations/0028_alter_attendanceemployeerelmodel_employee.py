# Generated by Django 3.2.9 on 2022-03-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0014_alter_employeesalarymodel_employee'),
        ('HRM_controller', '0027_rename_attendanceemployeeshiftmodel_attendanceshifttimemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceemployeerelmodel',
            name='employee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_employee_relation', to='HRM_Admin.employeeinformationmodel'),
        ),
    ]
