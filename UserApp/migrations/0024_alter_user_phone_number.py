# Generated by Django 3.2.9 on 2022-03-29 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0023_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]