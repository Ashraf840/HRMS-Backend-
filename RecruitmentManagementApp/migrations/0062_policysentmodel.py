# Generated by Django 3.2.9 on 2022-04-19 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0061_referenceinformationmodel_is_rejected'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolicySentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sent', models.BooleanField(default=False)),
                ('applicationId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sent_policy_application_id', to='RecruitmentManagementApp.userjobappliedmodel')),
            ],
        ),
    ]