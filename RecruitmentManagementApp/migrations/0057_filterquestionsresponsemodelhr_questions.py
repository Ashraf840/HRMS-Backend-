# Generated by Django 3.2.9 on 2022-03-28 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0056_alter_officialdocumentsmodel_applicationid'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterquestionsresponsemodelhr',
            name='questions',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='filter_questions', to='RecruitmentManagementApp.jobapplyfilterquestionmodel'),
            preserve_default=False,
        ),
    ]