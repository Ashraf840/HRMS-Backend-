# Generated by Django 3.2.9 on 2021-11-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0003_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useracademicinfomodel',
            name='cgpa',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=10),
            preserve_default=False,
        ),
    ]