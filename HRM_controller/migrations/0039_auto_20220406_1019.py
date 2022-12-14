# Generated by Django 3.2.9 on 2022-04-06 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0027_alter_user_phone_number'),
        ('HRM_controller', '0038_auto_20220405_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeepromotionmodel',
            name='designations',
        ),
        migrations.AddField(
            model_name='employeepromotionmodel',
            name='promotion_from',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='promotion_from', to='UserApp.userdesignationmodel'),
        ),
        migrations.AddField(
            model_name='employeepromotionmodel',
            name='promotion_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='promotion_to', to='UserApp.userdesignationmodel'),
        ),
    ]
