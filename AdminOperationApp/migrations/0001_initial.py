# Generated by Django 3.2.9 on 2021-12-28 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarkingDuringInterviewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('behavior', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('personality', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('dressSense', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('professionalism', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('engSpeaking', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('eagerness', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('flexibility', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('technicalKnowledge', models.CharField(blank=True, choices=[('5', 'A'), ('4', 'B'), ('3', 'C'), ('2', 'D'), ('1', 'E'), ('0', 'F')], max_length=10, null=True)),
                ('expSalary', models.CharField(blank=True, max_length=255, null=True)),
                ('expectedJoiningData', models.DateField(blank=True)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticalTestUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(blank=True, default=2)),
            ],
        ),
    ]
