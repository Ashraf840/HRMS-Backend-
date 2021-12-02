# Generated by Django 3.2.9 on 2021-12-02 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_validated',
            field=models.BooleanField(default=False, help_text='Designate if the user has Email Validate', verbose_name='Email Validate'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designate if the user has active status', verbose_name='Active Status'),
        ),
    ]
