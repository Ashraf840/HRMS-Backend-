# Generated by Django 3.2.9 on 2022-03-30 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0026_userdepartmentmodel_departmenthead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
