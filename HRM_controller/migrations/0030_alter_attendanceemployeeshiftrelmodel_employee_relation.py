# Generated by Django 3.2.9 on 2022-03-08 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0029_alter_employeeattendancelogmodel_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceemployeeshiftrelmodel',
            name='employee_relation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_relation', to='HRM_controller.attendanceemployeerelmodel'),
        ),
    ]
