# Generated by Django 3.2.9 on 2022-03-01 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0019_jobfilterquestionradiobuttonoptionmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobfilterquestionradiobuttonoptionmodel',
            name='jobId',
        ),
        migrations.AddField(
            model_name='jobfilterquestionradiobuttonoptionmodel',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='filter_question_option_job', to='RecruitmentManagementApp.jobapplyfilterquestionmodel'),
            preserve_default=False,
        ),
    ]