# Generated by Django 3.2.9 on 2021-12-04 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0007_auto_20211202_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfomodel',
            name='userSkills',
            field=models.ManyToManyField(related_name='user_skills', to='UserApp.SkillsModel'),
        ),
    ]
