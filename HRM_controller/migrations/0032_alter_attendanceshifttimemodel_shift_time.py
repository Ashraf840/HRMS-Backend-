# Generated by Django 3.2.9 on 2022-03-25 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_controller', '0031_auto_20220325_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendanceshifttimemodel',
            name='shift_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='HRM_controller.shifttimemodel'),
        ),
    ]
