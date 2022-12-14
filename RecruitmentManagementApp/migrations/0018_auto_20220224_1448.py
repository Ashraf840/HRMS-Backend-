# Generated by Django 3.2.9 on 2022-02-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0017_alter_practicaltestresponsemodel_practicaltestreslink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicaltestresponsemodel',
            name='practicalTestResFiles',
            field=models.FileField(blank=True, null=True, upload_to='practical_test/response/', verbose_name='Practical test response'),
        ),
        migrations.AlterField(
            model_name='practicaltestresponsemodel',
            name='practicalTestResLink',
            field=models.URLField(blank=True, verbose_name='Practical test response'),
        ),
    ]
