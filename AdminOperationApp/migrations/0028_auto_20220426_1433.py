# Generated by Django 3.2.9 on 2022-04-26 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0063_delete_policysentmodel'),
        ('AdminOperationApp', '0027_alter_interviewtimeschedulemodel_interviewtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewtimeschedulemodel',
            name='interviewTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='behavior',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='dressSense',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='eagerness',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='engSpeaking',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='flexibility',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='personality',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='professionalism',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='markingduringinterviewmodel',
            name='technicalKnowledge',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='practicaltestmarkinputmodel',
            name='testMark',
            field=models.CharField(blank=True, choices=[('A (Extremely Well)', 'A (Extremely Well)'), ('B (Modeartely Good)', 'B (Modeartely Good)'), ('C (Not up to the Mark)', 'C (Not up to the Mark)')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='PolicySentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sent', models.BooleanField(default=False)),
                ('applicationId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='policy_sent_application_id', to='RecruitmentManagementApp.userjobappliedmodel')),
            ],
        ),
    ]