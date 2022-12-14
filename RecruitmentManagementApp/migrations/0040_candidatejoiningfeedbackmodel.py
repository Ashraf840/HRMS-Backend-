# Generated by Django 3.2.9 on 2022-03-09 03:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0039_alter_referenceinformationmodel_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateJoiningFeedbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_agree', models.BooleanField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True)),
                ('applicationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_joining_feedback_application_id', to='RecruitmentManagementApp.userjobappliedmodel')),
            ],
        ),
    ]
