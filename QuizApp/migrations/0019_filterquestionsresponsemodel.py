# Generated by Django 3.2.9 on 2021-11-25 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0018_jobapplyfilterquestionmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterQuestionsResponseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(blank=True, max_length=255)),
                ('questions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_questions', to='QuizApp.jobapplyfilterquestionmodel')),
            ],
            options={
                'verbose_name_plural': 'Filter Question Response',
            },
        ),
    ]
