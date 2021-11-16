# Generated by Django 3.2.9 on 2021-11-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication_App', '0002_user_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='user',
            name='is_hr',
            field=models.BooleanField(default=False, help_text='Designate if the user has Hr status', verbose_name='Admin Status'),
        ),
    ]
