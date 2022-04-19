# Generated by Django 3.2.9 on 2022-04-12 03:58

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0028_user_signature_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signature_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='default.jpg', force_format='JPEG', help_text='Size Recommended: 300x80', keep_meta=True, quality=100, size=[512, 512], upload_to='users/'),
        ),
    ]
