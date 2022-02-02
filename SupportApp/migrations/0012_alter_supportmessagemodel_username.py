# Generated by Django 3.2.9 on 2022-02-02 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SupportApp', '0011_supportmessagemodel_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportmessagemodel',
            name='userName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_user_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
