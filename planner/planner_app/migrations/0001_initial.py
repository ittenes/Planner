# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 17:27
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
                'managed': False,
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'managed': True,
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('active', models.IntegerField()),
                ('owner_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.AuthUser')),
            ],
            options={
                'managed': True,
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='DayName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dayname', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'day_name',
            },
        ),
        migrations.CreateModel(
            name='Planning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.IntegerField()),
                ('user', models.IntegerField()),
                ('date', models.DateField()),
                ('hours', models.IntegerField()),
            ],
            options={
                'managed': True,
                'db_table': 'planning',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Client')),
            ],
            options={
                'managed': True,
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=250)),
                ('cif', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'managed': True,
                'db_table': 'provider',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(blank=True, null=True)),
                ('day_week_in', models.IntegerField(blank=True, null=True)),
                ('day_week_out', models.IntegerField(blank=True, null=True)),
                ('week_number', models.IntegerField(blank=True, null=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Project')),
            ],
            options={
                'managed': True,
                'db_table': 'request',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
            ],
            options={
                'managed': True,
                'db_table': 'schedule_company',
            },
        ),
        migrations.CreateModel(
            name='ScheduleCompanyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('schedule_company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.ScheduleCompany')),
            ],
            options={
                'managed': True,
                'db_table': 'schedule_company_user',
            },
        ),
        migrations.CreateModel(
            name='UserCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.Company')),
            ],
            options={
                'managed': True,
                'db_table': 'user_company',
            },
        ),
        migrations.CreateModel(
            name='UserHolidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany')),
            ],
            options={
                'managed': True,
                'db_table': 'user_holidays',
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
                'managed': True,
                'db_table': 'user_type',
            },
        ),
        migrations.CreateModel(
            name='WeekDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=250)),
                ('daywork', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.DayName')),
            ],
            options={
                'managed': True,
                'db_table': 'week_day',
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
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany'),
        ),
        migrations.AddField(
            model_name='schedulecompany',
            name='company_week_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.WeekDay'),
        ),
        migrations.AddField(
            model_name='request',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.UserCompany'),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.AuthUser'),
        ),
        migrations.AlterUniqueTogether(
            name='provider',
            unique_together=set([('company', 'cif')]),
        ),
        migrations.AlterUniqueTogether(
            name='planning',
            unique_together=set([('project', 'user', 'date')]),
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
            name='usercompany',
            unique_together=set([('email', 'company'), ('id', 'company')]),
        ),
        migrations.AlterUniqueTogether(
            name='schedulecompanyuser',
            unique_together=set([('user', 'schedule_company')]),
        ),
        migrations.AlterUniqueTogether(
            name='company',
            unique_together=set([('owner_company', 'name'), ('owner_company', 'active')]),
        ),
    ]
