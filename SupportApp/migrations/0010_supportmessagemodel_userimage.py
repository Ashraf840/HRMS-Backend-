# Generated by Django 3.2.9 on 2022-02-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SupportApp', '0009_auto_20220202_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportmessagemodel',
            name='userImage',
            field=models.URLField(blank=True),
        ),
    ]
