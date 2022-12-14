# Generated by Django 3.2.9 on 2022-02-17 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0018_alter_useracademicinfomodel_options'),
        ('HRM_Admin', '0008_trainingmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingmodel',
            name='training_department',
        ),
        migrations.AddField(
            model_name='trainingmodel',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_training_department', to='UserApp.userdepartmentmodel'),
        ),
        migrations.AddField(
            model_name='trainingmodel',
            name='passing_mark',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
