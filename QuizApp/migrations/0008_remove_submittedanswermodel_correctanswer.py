# Generated by Django 3.2.9 on 2021-11-25 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0007_submittedanswermodel_correctanswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submittedanswermodel',
            name='correctAnswer',
        ),
    ]
