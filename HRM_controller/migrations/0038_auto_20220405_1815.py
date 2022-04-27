# Generated by Django 3.2.9 on 2022-04-05 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0027_alter_user_phone_number'),
        ('HRM_controller', '0037_auto_20220405_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepromotionmodel',
            name='designations',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='UserApp.userdesignationmodel'),
        ),
        migrations.AlterField(
            model_name='employeepromotionmodel',
            name='promotion_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]