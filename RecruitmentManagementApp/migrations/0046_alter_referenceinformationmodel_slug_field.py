# Generated by Django 3.2.9 on 2022-03-10 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecruitmentManagementApp', '0045_auto_20220310_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referenceinformationmodel',
            name='slug_field',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]
