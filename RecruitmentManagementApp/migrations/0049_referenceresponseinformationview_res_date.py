# Generated by Django 3.2.9 on 2022-03-11 03:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0048_rename_refereeinformationmodel_referenceresponseinformationview'),
    ]

    operations = [
        migrations.AddField(
            model_name='referenceresponseinformationview',
            name='res_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
