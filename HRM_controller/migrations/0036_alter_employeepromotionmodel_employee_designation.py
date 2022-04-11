# Generated by Django 3.2.9 on 2022-04-05 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0027_alter_user_phone_number'),
        ('HRM_controller', '0035_employeepromotionmodel_employee_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepromotionmodel',
            name='employee_designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='total_designation', to='UserApp.userdesignationmodel'),
        ),
    ]
