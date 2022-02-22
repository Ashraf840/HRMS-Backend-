# Generated by Django 3.2.9 on 2022-02-22 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0010_employeeinformationmodel_shift'),
        ('HRM_controller', '0008_attendanceemployeeshiftmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendanceemployeerelmodel',
            name='signature_id',
        ),
        migrations.AlterField(
            model_name='attendanceemployeerelmodel',
            name='employee',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_relation', to='HRM_Admin.employeeinformationmodel'),
        ),
        migrations.CreateModel(
            name='AttendanceEmployeeShiftRelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_relation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_relation', to='HRM_controller.attendanceemployeerelmodel')),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_employee_shift', to='HRM_controller.attendanceemployeeshiftmodel')),
            ],
        ),
    ]
