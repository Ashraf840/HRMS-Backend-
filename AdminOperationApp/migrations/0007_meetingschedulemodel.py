# Generated by Django 3.2.9 on 2022-01-05 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AdminOperationApp', '0006_alter_practicaltestmarkinputmodel_jobapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetingDateTime', models.DateTimeField()),
                ('scheduleAssignDate', models.DateField(auto_now_add=True)),
                ('applicationId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='application_id_applied_job', to='RecruitmentManagementApp.userjobappliedmodel')),
                ('meetingGuest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting_guest_user', to=settings.AUTH_USER_MODEL)),
                ('meetingHost', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting_host_user', to=settings.AUTH_USER_MODEL)),
                ('meetingScheduleBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meeting_scheduled_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
