# Generated by Django 3.2.9 on 2022-03-04 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0026_remove_employeeattendancelogmodel_reg_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AttendanceEmployeeShiftModel',
            new_name='AttendanceShiftTimeModel',
        ),
    ]