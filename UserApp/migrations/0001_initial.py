# Generated by Django 3.2.9 on 2021-11-21 10:18

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
                ('phone_number', models.IntegerField(null=True)),
                ('nid', models.IntegerField(null=True)),
                ('nationality', models.CharField(max_length=50, null=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('birthDate', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20, verbose_name='Choose Gender')),
                ('is_staff', models.BooleanField(default=False, help_text='Designate if the user has staff status', verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, help_text='Designate if the user has active status', verbose_name='Active Status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designate if the user has superuser status', verbose_name='Superuser Status')),
                ('is_job_post_permission', models.BooleanField(default=False, help_text='Designate if the user has Hr status', verbose_name='Hr Status')),
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
            name='UserWorkingExperienceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizationName', models.CharField(max_length=255, null=True)),
                ('department', models.CharField(max_length=255, null=True)),
                ('position', models.CharField(max_length=255, null=True)),
                ('joinDate', models.DateField(null=True)),
                ('quitDate', models.DateField(null=True)),
                ('responsibility', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_experience_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Work Experience',
            },
        ),
        migrations.CreateModel(
            name='UserTrainingExperienceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorName', models.CharField(max_length=255)),
                ('topicName', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_info_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Training Information',
            },
        ),
        migrations.CreateModel(
            name='UserInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField(null=True)),
                ('shift', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], max_length=20, verbose_name='Choose Shift')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_user', to='UserApp.userdepartmentmodel')),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='designation_user', to='UserApp.userdepartmentmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info_user', to=settings.AUTH_USER_MODEL)),
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
        migrations.CreateModel(
            name='UserCertificationsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendorName', models.CharField(max_length=255)),
                ('examName', models.CharField(max_length=255)),
                ('score', models.CharField(max_length=255)),
                ('certificationId', models.CharField(max_length=255)),
                ('dateOfAchievement', models.DateField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certification_info_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Certification Information',
            },
        ),
        migrations.CreateModel(
            name='UserAcademicInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educationLevel', models.CharField(max_length=255, null=True)),
                ('degreeTitle', models.CharField(max_length=255, null=True)),
                ('instituteName', models.CharField(max_length=255, null=True)),
                ('major', models.CharField(max_length=255, null=True)),
                ('year', models.DateField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('cgpa', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='academic_info_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Academic Information',
            },
        ),
        migrations.CreateModel(
            name='JobPreferenceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferredPost', models.CharField(max_length=255)),
                ('preferredShift', models.CharField(max_length=255)),
                ('salaryFrom', models.IntegerField()),
                ('salaryTo', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_preference_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlackListedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('token', 'user')},
            },
        ),
    ]
