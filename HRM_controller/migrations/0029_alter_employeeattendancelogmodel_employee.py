# Generated by Django 3.2.9 on 2022-03-08 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0028_alter_attendanceemployeerelmodel_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendancelogmodel',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_attendance_log', to='HRM_controller.attendanceemployeerelmodel'),
        ),
    ]
