# Generated by Django 3.2.9 on 2022-10-19 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0049_holidaymodel_month'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeepromotionmodel',
            old_name='promotion_form',
            new_name='promotion_from',
        ),
    ]