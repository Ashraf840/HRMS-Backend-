# Generated by Django 3.2.9 on 2022-03-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0035_alter_referenceinformationmodel_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referenceinformationmodel',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='referenceinformationmodel',
            name='phoneNumber',
            field=models.IntegerField(max_length=15),
        ),
    ]
