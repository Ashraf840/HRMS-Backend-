# Generated by Django 3.2.9 on 2022-03-30 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0025_userdesignationmodel_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdepartmentmodel',
            name='departmentHead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_head_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
