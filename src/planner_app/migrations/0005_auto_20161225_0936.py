# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-25 09:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner_app', '0004_auto_20161224_1212'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='Petition',
        ),
        migrations.AlterModelOptions(
            name='petition',
            options={'managed': True, 'verbose_name_plural': 'Petition'},
        ),
        migrations.AlterModelTable(
            name='petition',
            table='petition',
        ),
    ]
