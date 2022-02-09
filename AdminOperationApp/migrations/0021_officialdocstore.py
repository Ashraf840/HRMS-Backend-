# Generated by Django 3.2.9 on 2022-02-03 06:22

import AdminOperationApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminOperationApp', '0020_commentsondocumentsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficialDocStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docName', models.CharField(max_length=50)),
                ('docFile', models.FileField(upload_to=AdminOperationApp.models.doc_file_name)),
            ],
        ),
    ]