# Generated by Django 3.2.9 on 2021-12-07 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0017_auto_20211206_1744'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlinetestresponsemodel',
            name='jobId',
        ),
        migrations.RemoveField(
            model_name='practicaltestresponsemodel',
            name='jobId',
        ),
        migrations.AddField(
            model_name='onlinetestresponsemodel',
            name='appliedJob',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_online_response', to='RecruitmentManagementApp.userjobappliedmodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='practicaltestresponsemodel',
            name='appliedJob',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_practical_response', to='RecruitmentManagementApp.userjobappliedmodel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userjobappliedmodel',
            name='jobPostId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_job_post_id', to='RecruitmentManagementApp.jobpostmodel'),
        ),
    ]
