# Generated by Django 3.2.9 on 2022-04-06 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0039_auto_20220406_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeepromotionmodel',
            name='promotion_date',
            field=models.DateField(),
        ),
    ]