# Generated by Django 3.2.9 on 2021-12-22 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_alter_user_nid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdepartmentmodel',
            name='deptManager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
