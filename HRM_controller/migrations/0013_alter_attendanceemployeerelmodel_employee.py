# Generated by Django 3.2.9 on 2022-02-22 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0010_employeeinformationmodel_shift'),
        ('HRM_controller', '0012_attendanceemployeerelmodel_attendanceemployeeshiftrelmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceemployeerelmodel',
            name='employee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_relation', to='HRM_Admin.employeeinformationmodel'),
        ),
    ]