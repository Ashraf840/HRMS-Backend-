# Generated by Django 3.2.9 on 2022-02-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0020_holidaymodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='holidaymodel',
            old_name='date',
            new_name='h_date',
        ),
        migrations.AddField(
            model_name='holidaymodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
