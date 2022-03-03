# Generated by Django 3.2.9 on 2022-02-24 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_User', '0002_leaverequestmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequestmodel',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('canceled', 'Canceled')], default='pending', max_length=50),
        ),
    ]