# Generated by Django 3.2.9 on 2022-01-04 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_auto_20220104_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='degreetitlemodel',
            name='educationLevel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='education_level_education', to='UserApp.educationlevelmodel'),
            preserve_default=False,
        ),
    ]
