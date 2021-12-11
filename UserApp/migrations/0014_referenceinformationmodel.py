# Generated by Django 3.2.9 on 2021-12-09 06:29

import UserApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0013_auto_20211209_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferenceInformationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phoneNumber', models.IntegerField()),
                ('relationWithReferer', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('attachedFile', models.FileField(upload_to=UserApp.models.content_file_name)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_information_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]