# Generated by Django 3.2.9 on 2021-11-17 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDepartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Department',
            },
        ),
        migrations.CreateModel(
            name='UserDesignationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Designation',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('profile_pic', models.ImageField(default='users/default.jpg', upload_to='users/')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20, verbose_name='Choose Gender')),
                ('is_staff', models.BooleanField(default=False, help_text='Designate if the user has staff status', verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, help_text='Designate if the user has active status', verbose_name='Active Status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designate if the user has superuser status', verbose_name='Superuser Status')),
                ('is_hr', models.BooleanField(default=False, help_text='Designate if the user has Hr status', verbose_name='Hr Status')),
                ('is_employee', models.BooleanField(default=False, help_text='Designate if the user has Employee status', verbose_name='Employee Status')),
                ('is_candidate', models.BooleanField(default=False, help_text='Designate if the user has Candidate status', verbose_name='candidate Status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(null=True)),
                ('salary', models.IntegerField(null=True)),
                ('shift', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], max_length=20, verbose_name='Choose Shift')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_department', to='User_App.userdepartmentmodel')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_designation', to='User_App.userdepartmentmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='permission_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User_Info',
            },
        ),
        migrations.AddField(
            model_name='userdepartmentmodel',
            name='deptManager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
