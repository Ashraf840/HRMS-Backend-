# Generated by Django 3.2.9 on 2022-02-09 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0014_auto_20220207_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicaltestmodel',
            name='practicalFile',
            field=models.FileField(blank=True, upload_to='users/files', verbose_name='Practical Test File'),
        ),
    ]