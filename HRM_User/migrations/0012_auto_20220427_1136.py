# Generated by Django 3.2.9 on 2022-04-27 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_User', '0011_remove_exitinterviewanswermodel_ok'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resignationmodel',
            name='employee',
        ),
        migrations.DeleteModel(
            name='ExitInterviewAnswerModel',
        ),
        migrations.DeleteModel(
            name='ExitInterviewQuestionModel',
        ),
        migrations.DeleteModel(
            name='ResignationModel',
        ),
    ]
