# Generated by Django 3.2.9 on 2022-01-20 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AdminOperationApp', '0016_generateappointmentlettermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewtimeschedulemodel',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='candidate_interview_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
