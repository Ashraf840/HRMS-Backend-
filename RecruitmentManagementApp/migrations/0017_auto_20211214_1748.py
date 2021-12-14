# Generated by Django 3.2.9 on 2021-12-14 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RecruitmentManagementApp', '0016_auto_20211206_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobStatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('statusOrder', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='onlinetestresponsemodel',
            name='jobId',
        ),
        migrations.RemoveField(
            model_name='practicaltestmodel',
            name='practicalQuestion',
        ),
        migrations.RemoveField(
            model_name='practicaltestresponsemodel',
            name='jobId',
        ),
        migrations.AddField(
            model_name='onlinetestresponsemodel',
            name='appliedJob',
            field=models.OneToOneField(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_online_response', to='RecruitmentManagementApp.userjobappliedmodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='onlinetestresponsemodel',
            name='submittedTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='practicaltestmodel',
            name='practicalFile',
            field=models.FileField(default=2, upload_to='users/files', verbose_name='Practical Test File'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='practicaltestmodel',
            name='testLink',
            field=models.URLField(blank=True, verbose_name='Test link'),
        ),
        migrations.AddField(
            model_name='practicaltestmodel',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='practical_user_info', to='UserApp.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='practicaltestresponsemodel',
            name='appliedJob',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_practical_response', to='RecruitmentManagementApp.userjobappliedmodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='practicaltestresponsemodel',
            name='submittedTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userjobappliedmodel',
            name='appliedDate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='onlinetestresponsemodel',
            name='analyticalTestMark',
            field=models.IntegerField(blank=True, verbose_name='Analytical Test Mark'),
        ),
        migrations.AlterField(
            model_name='onlinetestresponsemodel',
            name='analyticalTestScnSrt',
            field=models.ImageField(blank=True, upload_to='online_test/analytical_test/', verbose_name='Screenshot'),
        ),
        migrations.AlterField(
            model_name='onlinetestresponsemodel',
            name='practicalTestMark',
            field=models.IntegerField(blank=True, verbose_name='Practical Test Mark'),
        ),
        migrations.AlterField(
            model_name='onlinetestresponsemodel',
            name='practicalTestScnSrt',
            field=models.ImageField(blank=True, upload_to='online_test/practical_test/', verbose_name='Screenshot'),
        ),
        migrations.AlterField(
            model_name='practicaltestmodel',
            name='jobInfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='practical_job_info', to='RecruitmentManagementApp.jobpostmodel'),
        ),
        migrations.AlterField(
            model_name='userjobappliedmodel',
            name='jobPostId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_job_post_id', to='RecruitmentManagementApp.jobpostmodel'),
        ),
        migrations.AlterField(
            model_name='userjobappliedmodel',
            name='jobProgressStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_progress_status', to='RecruitmentManagementApp.jobstatusmodel'),
        ),
    ]
