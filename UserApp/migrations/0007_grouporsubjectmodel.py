# Generated by Django 3.2.9 on 2022-01-04 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0006_degreetitlemodel_educationlevel'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupOrSubjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('majorGroup', models.CharField(max_length=100)),
                ('educationLevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='major_group_educational_level', to='UserApp.educationlevelmodel')),
            ],
        ),
    ]
