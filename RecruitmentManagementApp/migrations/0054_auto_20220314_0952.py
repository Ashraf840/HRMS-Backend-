# Generated by Django 3.2.9 on 2022-03-14 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0053_auto_20220311_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobpostmodel',
            old_name='jobDescription',
            new_name='jobOverview',
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='jobRequirements',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='jobResponsibilities',
            field=models.TextField(null=True),
        ),
    ]
