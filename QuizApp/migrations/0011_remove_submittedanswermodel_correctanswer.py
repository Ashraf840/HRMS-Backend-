# Generated by Django 3.2.9 on 2021-11-25 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0010_submittedanswermodel_correctanswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submittedanswermodel',
            name='correctAnswer',
        ),
    ]
