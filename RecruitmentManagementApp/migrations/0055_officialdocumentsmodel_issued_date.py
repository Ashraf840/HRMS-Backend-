# Generated by Django 3.2.9 on 2022-03-14 05:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0054_auto_20220314_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='officialdocumentsmodel',
            name='issued_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
