# Generated by Django 3.2.9 on 2021-12-09 05:01

import UserApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0011_auto_20211208_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSubmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sscCertificate', models.FileField(upload_to='document/ssc/')),
                ('hscCertificate', models.FileField(upload_to='document/hsc/')),
                ('graduationCertificate', models.FileField(upload_to='document/graduation/')),
                ('postGraduationCertificate', models.FileField(blank=True, upload_to='document/postGraduation/')),
                ('nidCard', models.FileField(blank=True, upload_to='document/nid/')),
                ('userPassportImage', models.ImageField(upload_to=UserApp.models.content_file_name)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='document_submission_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]