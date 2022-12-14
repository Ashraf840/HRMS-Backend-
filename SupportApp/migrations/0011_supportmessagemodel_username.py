# Generated by Django 3.2.9 on 2022-02-02 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SupportApp', '0010_supportmessagemodel_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportmessagemodel',
            name='userName',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='message_user_name', to='UserApp.user'),
            preserve_default=False,
        ),
    ]
