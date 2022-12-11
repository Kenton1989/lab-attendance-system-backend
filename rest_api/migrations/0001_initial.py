# Generated by Django 4.1.4 on 2022-12-11 23:18

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
import rest_api.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters and digits only.', max_length=150, unique=True, validators=[rest_api.validators.username_validator], verbose_name='username')),
                ('display_name', models.CharField(blank=True, max_length=150, verbose_name='display name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into the Django admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='group name')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MakeUpRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('is_compulsory', models.BooleanField(default=True)),
                ('allow_late_check_in', models.BooleanField(default=True)),
                ('check_in_deadline', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_state', models.CharField(choices=[('absent', 'absent'), ('attend', 'attend')], default='absent', max_length=20)),
                ('check_in_datetime', models.DateTimeField(blank=True)),
                ('last_modify', models.DateTimeField(default=django.utils.timezone.now)),
                ('remark', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_state', models.CharField(choices=[('absent', 'absent'), ('attend', 'attend')], default='absent', max_length=20)),
                ('check_in_datetime', models.DateTimeField(blank=True)),
                ('last_modify', models.DateTimeField(default=django.utils.timezone.now)),
                ('remark', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('monday', models.DateField(validators=[rest_api.validators.monday_validator])),
                ('next_monday', models.DateField(validators=[rest_api.validators.monday_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='lab_info', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('room_count', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='week',
            constraint=models.CheckConstraint(check=models.Q(('next_monday', django.db.models.expressions.CombinedExpression(models.F('monday'), '+', models.Value(datetime.timedelta(days=7))))), name='ensure_7_days_gap', violation_error_message='next_monday must be exactly 7 days greater then monday'),
        ),
        migrations.AddField(
            model_name='teacherattendance',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_attendances', to='rest_api.session'),
        ),
        migrations.AddField(
            model_name='teacherattendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_attendances', to='rest_api.session'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='session',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='rest_api.group'),
        ),
        migrations.AddField(
            model_name='session',
            name='make_up_students',
            field=models.ManyToManyField(related_name='make_up_sessions', through='rest_api.MakeUpRelationship', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='makeuprelationship',
            name='make_up_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rest_api.session'),
        ),
        migrations.AddField(
            model_name='makeuprelationship',
            name='original_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rest_api.session'),
        ),
        migrations.AddField(
            model_name='makeuprelationship',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='groupstudent',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='rest_api.group'),
        ),
        migrations.AddField(
            model_name='groupstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='rest_api.course'),
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(related_name='student_of_groups', through='rest_api.GroupStudent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='supervisors',
            field=models.ManyToManyField(related_name='supervisor_of_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='teachers',
            field=models.ManyToManyField(related_name='teacher_of_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='coordinators',
            field=models.ManyToManyField(related_name='coordinator_of_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='teacherattendance',
            constraint=models.UniqueConstraint(fields=('session', 'user'), name='unique_teacher_attendance_session', violation_error_message='Only one attendance record allowed per session per teacher.'),
        ),
        migrations.AddConstraint(
            model_name='studentattendance',
            constraint=models.UniqueConstraint(fields=('session', 'user'), name='unique_student_attendance_session', violation_error_message='Only one attendance record allowed per session per student.'),
        ),
        migrations.AddField(
            model_name='session',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='rest_api.lab'),
        ),
        migrations.AddConstraint(
            model_name='makeuprelationship',
            constraint=models.UniqueConstraint(fields=('student', 'original_session'), name='unique_original_session_student', violation_error_message='Student can make up a session using only one another session.'),
        ),
        migrations.AddConstraint(
            model_name='makeuprelationship',
            constraint=models.UniqueConstraint(fields=('student', 'make_up_session'), name='unique_make_up_session_student', violation_error_message='Student can only participate one session for at most once.'),
        ),
        migrations.AddField(
            model_name='lab',
            name='executives',
            field=models.ManyToManyField(related_name='executive_of_labs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='groupstudent',
            constraint=models.UniqueConstraint(fields=('group', 'student'), name='unique_group_student', violation_error_message='Student should be unique under a group.'),
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('course', 'name'), name='unique_course_group', violation_error_message='Group name should be unique under a course.'),
        ),
        migrations.AddConstraint(
            model_name='session',
            constraint=models.CheckConstraint(check=models.Q(('end_datetime_gte', models.Q('start_datetime'))), name='session_end_datetime_after_start_datetime', violation_error_message='end_datetime must be greater than start_datetime'),
        ),
    ]
