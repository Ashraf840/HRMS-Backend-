# Generated by Django 3.2.9 on 2021-12-28 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('QuizApp', '0002_initial'),
        ('UserApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RecruitmentManagementApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userjobappliedmodel',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='referenceinformationmodel',
            name='applied_job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='references_submission_applied_job', to='RecruitmentManagementApp.userjobappliedmodel'),
        ),
        migrations.AddField(
            model_name='referenceinformationmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_information_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practicaltestresponsemodel',
            name='appliedJob',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_practical_response', to='RecruitmentManagementApp.userjobappliedmodel'),
        ),
        migrations.AddField(
            model_name='practicaltestresponsemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practical_response_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='practicaltestmodel',
            name='jobInfo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='practical_job_info', to='RecruitmentManagementApp.jobpostmodel'),
        ),
        migrations.AddField(
            model_name='practicaltestmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='practical_user_info', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinetestresponsemodel',
            name='appliedJob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applied_online_response', to='RecruitmentManagementApp.userjobappliedmodel'),
        ),
        migrations.AddField(
            model_name='onlinetestresponsemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='online_response_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinetestmodel',
            name='jobInfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_info_online', to='RecruitmentManagementApp.jobpostmodel'),
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_jobPost', to='UserApp.userdepartmentmodel'),
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='filterQuestions',
            field=models.ManyToManyField(related_name='filter_question_list', to='QuizApp.JobApplyFilterQuestionModel'),
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='jobProgressStatus',
            field=models.ManyToManyField(related_name='job_progress_statusM2M', to='RecruitmentManagementApp.JobStatusModel'),
        ),
        migrations.AddField(
            model_name='jobpostmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_post_model', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='filterquestionsresponsemodelhr',
            name='jobPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_info', to='RecruitmentManagementApp.jobpostmodel'),
        ),
        migrations.AddField(
            model_name='filterquestionsresponsemodelhr',
            name='questions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_questions', to='QuizApp.jobapplyfilterquestionmodel'),
        ),
        migrations.AddField(
            model_name='filterquestionsresponsemodelhr',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='response_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentsubmissionmodel',
            name='applied_job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='document_submission_applied_job', to='RecruitmentManagementApp.userjobappliedmodel'),
        ),
        migrations.AddField(
            model_name='documentsubmissionmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_submission_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
