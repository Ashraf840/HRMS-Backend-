# Generated by Django 3.2.9 on 2021-12-28 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminOperationApp', '0001_initial'),
        ('RecruitmentManagementApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicaltestusermodel',
            name='practicalTestInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practical_test_info', to='RecruitmentManagementApp.practicaltestmodel'),
        ),
    ]
