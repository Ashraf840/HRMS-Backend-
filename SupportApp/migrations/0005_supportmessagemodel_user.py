# Generated by Django 3.2.9 on 2022-01-18 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SupportApp', '0004_auto_20220118_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportmessagemodel',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='message_user', to='UserApp.user'),
            preserve_default=False,
        ),
    ]
