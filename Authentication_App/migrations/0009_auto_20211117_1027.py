# Generated by Django 3.2.9 on 2021-11-17 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication_App', '0008_auto_20211116_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfomodel',
            options={'verbose_name_plural': 'User_Info'},
        ),
        migrations.AlterField(
            model_name='user',
            name='is_candidate',
            field=models.BooleanField(default=False, help_text='Designate if the user has Candidate status', verbose_name='candidate Status'),
        ),
    ]
