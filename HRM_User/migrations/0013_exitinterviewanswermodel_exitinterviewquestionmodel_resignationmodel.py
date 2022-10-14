# Generated by Django 3.2.9 on 2022-04-27 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0016_employeeinformationmodel_personal_email'),
        ('HRM_User', '0012_auto_20220427_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExitInterviewQuestionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('bool', 'Bool')], default='text', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ResignationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('resignationDate', models.DateField(auto_now_add=True)),
                ('noticeDate', models.DateField()),
                ('resignationstaus', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending', max_length=50)),
                ('resignatioAcceptDate', models.DateField(blank=True, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resignation_employee', to='HRM_Admin.employeeinformationmodel')),
            ],
        ),
        migrations.CreateModel(
            name='ExitInterviewAnswerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='HRM_User.exitinterviewquestionmodel')),
                ('resignation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_employee', to='HRM_User.resignationmodel')),
            ],
        ),
    ]
