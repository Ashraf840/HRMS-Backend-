# Generated by Django 3.2.9 on 2022-02-03 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminOperationApp', '0021_officialdocstore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generateappointmentlettermodel',
            name='jobDescription',
        ),
        migrations.RemoveField(
            model_name='generateappointmentlettermodel',
            name='termsCondition',
        ),
    ]
