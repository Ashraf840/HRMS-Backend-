# Generated by Django 3.2.9 on 2022-02-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0018_alter_useracademicinfomodel_options'),
        ('HRM_controller', '0005_merge_20220217_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('attachment', models.FileField(upload_to='')),
                ('department', models.ManyToManyField(related_name='notice_department', to='UserApp.UserDepartmentModel')),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('department', models.ManyToManyField(related_name='announcement_department', to='UserApp.UserDepartmentModel')),
            ],
        ),
    ]
