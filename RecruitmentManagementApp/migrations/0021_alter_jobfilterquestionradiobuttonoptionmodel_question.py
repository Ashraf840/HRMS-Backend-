# Generated by Django 3.2.9 on 2022-03-01 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0020_auto_20220301_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobfilterquestionradiobuttonoptionmodel',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_question_option_job', to='RecruitmentManagementApp.jobapplyfilterquestionmodel'),
        ),
    ]