# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-18 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
                'verbose_name_plural': 'AuthUsers',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'client',
                'managed': True,
                'verbose_name_plural': 'Clients',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('active', models.IntegerField()),
                ('slug', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.AuthUser')),
            ],
            options={
                'db_table': 'company',
                'managed': True,
                'verbose_name_plural': 'Companys',
            },
        ),
        migrations.CreateModel(
            name='DayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayname', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'day_name',
                'managed': True,
                'verbose_name_plural': 'DayNames',
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField(blank=True, null=True)),
                ('dayweek', models.IntegerField()),
                ('hours', models.IntegerField()),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'db_table': 'planning',
                'managed': True,
                'verbose_name_plural': 'Plannings',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Client')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'db_table': 'project',
                'managed': True,
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cif', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'db_table': 'provider',
                'managed': True,
                'verbose_name_plural': 'Providers',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(null=True)),
                ('day_week_in', models.IntegerField(null=True)),
                ('day_week_out', models.IntegerField(null=True)),
                ('week_number', models.IntegerField(null=True)),
                ('planned', models.BooleanField(default=False)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Project')),
            ],
            options={
                'db_table': 'request',
                'managed': True,
                'verbose_name_plural': 'Requests',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'role',
                'managed': True,
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'db_table': 'schedule_company',
                'managed': True,
                'verbose_name_plural': 'ScheduleCompanys',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCompanyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField()),
                ('schedule_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.ScheduleCompany')),
            ],
            options={
                'db_table': 'schedule_company_user',
                'managed': True,
                'verbose_name_plural': 'ScheduleCompanyUsers',
            },
        ),
        migrations.CreateModel(
            name='UserCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(max_length=50)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'db_table': 'user_company',
                'managed': True,
                'verbose_name_plural': 'UserCompanys',
            },
        ),
        migrations.CreateModel(
            name='UserHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField(null=True)),
                ('week', models.IntegerField(blank=True, null=True)),
                ('schedule_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.ScheduleCompany')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany')),
            ],
            options={
                'db_table': 'user_holidays',
                'managed': True,
                'verbose_name_plural': 'UserHolidayss',
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_user', models.CharField(blank=True, max_length=50, null=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Role')),
            ],
            options={
                'db_table': 'user_type',
                'managed': True,
                'verbose_name_plural': 'UserTypes',
            },
        ),
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
                ('daywork', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.DayName')),
            ],
            options={
                'db_table': 'week_day',
                'managed': True,
                'verbose_name_plural': 'WeekDays',
            },
        ),
        migrations.AddField(
            model_name='usercompany',
            name='type_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserType'),
        ),
        migrations.AddField(
            model_name='usercompany',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.AuthUser'),
        ),
        migrations.AddField(
            model_name='schedulecompanyuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany'),
        ),
        migrations.AddField(
            model_name='schedulecompany',
            name='company_week_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.WeekDay'),
        ),
        migrations.AddField(
            model_name='request',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany'),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.AuthUser'),
        ),
        migrations.AddField(
            model_name='planning',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Project'),
        ),
        migrations.AddField(
            model_name='planning',
            name='resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany'),
        ),
        migrations.AddField(
            model_name='client',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company'),
        ),
        migrations.AlterUniqueTogether(
            name='weekday',
            unique_together=set([('daywork', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='userholidays',
            unique_together=set([('user', 'schedule_company', 'week')]),
        ),
        migrations.AlterUniqueTogether(
            name='usercompany',
            unique_together=set([('id', 'company'), ('email', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='schedulecompanyuser',
            unique_together=set([('user', 'schedule_company')]),
        ),
        migrations.AlterUniqueTogether(
            name='schedulecompany',
            unique_together=set([('company_week_day', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='provider',
            unique_together=set([('company', 'cif')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('name', 'company'), ('name', 'client')]),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set([('user', 'name'), ('user', 'active')]),
        ),
    ]