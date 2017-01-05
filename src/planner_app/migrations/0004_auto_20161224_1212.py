# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-24 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planner_app', '0003_auto_20161224_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75, null=True)),
            ],
            options={
                'db_table': 'project_status',
                'managed': True,
                'verbose_name_plural': 'ProjectsStatus',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='planner_app.ProjectStatus'),
            preserve_default=False,
        ),
    ]