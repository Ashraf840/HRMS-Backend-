# Generated by Django 3.2.9 on 2021-12-30 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminOperationApp', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='markingduringinterviewmodel',
            old_name='user',
            new_name='candidate',
        ),
    ]
