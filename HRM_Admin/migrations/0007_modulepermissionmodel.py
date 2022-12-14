# Generated by Django 3.2.9 on 2022-02-16 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HRM_Admin', '0006_remove_employeeinformationmodel_official_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModulePermissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_ceo', models.BooleanField(default=False)),
                ('is_gm', models.BooleanField(default=False)),
                ('is_hrm', models.BooleanField(default=False)),
                ('is_hre', models.BooleanField(default=False)),
                ('is_accountant', models.BooleanField(default=False)),
                ('is_pm', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='module_permission_employee', to='HRM_Admin.employeeinformationmodel')),
            ],
        ),
    ]
