# Generated by Django 3.2.9 on 2022-03-10 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0042_auto_20220309_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceQuestionsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='refereeinformationmodel',
            name='address_of_company',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='refereeinformationmodel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='refereeinformationmodel',
            name='job_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='refereeinformationmodel',
            name='name_of_company',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='ReferencesQuestionResponseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_response_qus', to='RecruitmentManagementApp.referencequestionsmodel')),
                ('referee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referee_information', to='RecruitmentManagementApp.refereeinformationmodel')),
            ],
        ),
    ]
