# Generated by Django 3.2.9 on 2022-02-23 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0021_auto_20220223_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holidaymodel',
            old_name='h_date',
            new_name='holiday_date',
        ),
    ]