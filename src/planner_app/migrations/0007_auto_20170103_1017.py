# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 10:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner_app', '0006_auto_20161228_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petition',
            old_name='year_pet',
            new_name='year',
        ),
        migrations.RenameField(
            model_name='planning',
            old_name='year_plan',
            new_name='year',
        ),
    ]