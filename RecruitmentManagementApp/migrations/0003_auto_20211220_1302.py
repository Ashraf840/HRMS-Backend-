# Generated by Django 3.2.9 on 2021-12-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicaltestresponsemodel',
            name='practicalTestResFiles',
            field=models.ImageField(blank=True, upload_to='practical_test/response/'),
        ),
        migrations.AlterField(
            model_name='practicaltestresponsemodel',
            name='practicalTestResLink',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]