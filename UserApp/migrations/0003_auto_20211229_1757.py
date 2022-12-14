# Generated by Django 3.2.9 on 2021-12-29 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_auto_20211229_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeinfomodel',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_user', to='UserApp.userdepartmentmodel'),
        ),
        migrations.AlterField(
            model_name='employeeinfomodel',
            name='designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='designation_user', to='UserApp.userdesignationmodel'),
        ),
        migrations.AlterField(
            model_name='employeeinfomodel',
            name='salary',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
