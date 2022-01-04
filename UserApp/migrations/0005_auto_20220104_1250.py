# Generated by Django 3.2.9 on 2022-01-04 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0004_rename_personalemail_employeeinfomodel_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeTitleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EducationLevelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educationLevel', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='useracademicinfomodel',
            name='degreeTitle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='degree_title', to='UserApp.degreetitlemodel'),
        ),
        migrations.AlterField(
            model_name='useracademicinfomodel',
            name='educationLevel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='education_level', to='UserApp.educationlevelmodel'),
        ),
    ]
