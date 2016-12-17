# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import datetime


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()


    def __str__(self): return self.email

    class Meta:
        managed = False
        db_table = 'auth_user'
        verbose_name_plural = 'AuthUsers'


class Client(models.Model):
    name = models.CharField(max_length=250)
    company = models.ForeignKey('Company', models.DO_NOTHING,)


    def __str__(self): return self.name

    class Meta:
        managed = False
        db_table = 'client'
        verbose_name_plural = 'Clients'

class Company(models.Model):
    name = models.CharField(max_length=75)
    owner_company = models.ForeignKey('AuthUser', models.DO_NOTHING)
    active = models.IntegerField()


    def __str__(self): return self.name

    class Meta:
        managed = False
        db_table = 'company'
        unique_together = (('owner_company', 'name'), ('owner_company', 'active'))
        verbose_name_plural = 'Companys'


class Planning(models.Model):
    project = models.ForeignKey('Project', models.DO_NOTHING,)
    resource = models.ForeignKey('UserCompany', models.DO_NOTHING, blank=False, null=True)
    week = models.IntegerField(blank=True, null=True)
    dayweek = models.IntegerField()
    hours = models.IntegerField()
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    class Meta:
        managed = False
        db_table = 'planning'
        verbose_name_plural = 'Plannings'



class Project(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING,)
    name = models.CharField(max_length=50, blank=True, null=True)
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)


    def __str__(self): return self.name

    class Meta:
        managed = False
        db_table = 'project'
        unique_together = (('name', 'client'),('name', 'company'),)
        verbose_name_plural = 'Projects'

class Provider(models.Model):
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    cif = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'provider'
        unique_together = (('company', 'cif'),)
        verbose_name_plural = 'Providers'


class Request(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING,blank=False, null=True)
    project = models.ForeignKey('Project', models.DO_NOTHING, blank=False, null=True)
    time = models.IntegerField(blank=False, null=True)
    resource = models.ForeignKey('UserCompany', models.DO_NOTHING, blank=False, null=True)
    day_week_in = models.IntegerField(null=True)
    day_week_out = models.IntegerField(blank=False, null=True)
    week_number = models.IntegerField(blank=False, null=True)
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    planned = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'request'
        verbose_name_plural = 'Requests'

class Role(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'
        verbose_name_plural = 'Roles'


class ScheduleCompany(models.Model):
    company_week_day = models.ForeignKey('WeekDay', models.DO_NOTHING)
    hours = models.IntegerField()
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)

    def __str__(self):
        srtday = str(self.company_week_day)
        return srtday

    class Meta:
        managed = False
        db_table = 'schedule_company'
        unique_together = (('company_week_day', 'company'),)
        verbose_name_plural = 'ScheduleCompanys'


class ScheduleCompanyUser(models.Model):
    user = models.ForeignKey('UserCompany', models.DO_NOTHING, null=True)
    schedule_company = models.ForeignKey(ScheduleCompany, models.DO_NOTHING)
    hour = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'schedule_company_user'
        unique_together = (('user', 'schedule_company'),)
        verbose_name_plural = 'ScheduleCompanyUsers'


class UserCompany(models.Model):
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    type_user = models.ForeignKey('UserType', models.DO_NOTHING,)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    email = models.CharField(max_length=50)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING,blank=True, null=True)


    def __str__(self): return self.first_name

    class Meta:
        managed = False
        db_table = 'user_company'
        unique_together = (('email', 'company'), ('id', 'company'),)
        verbose_name_plural = 'UserCompanys'


class UserHolidays(models.Model):
    user = models.ForeignKey('UserCompany', models.DO_NOTHING, null=True)
    schedule_company = models.ForeignKey(ScheduleCompany, models.DO_NOTHING)
    hour = models.IntegerField(null=True)
    week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_holidays'
        unique_together = (('user', 'schedule_company','week'),)
        verbose_name_plural = 'UserHolidayss'


class UserType(models.Model):
    type_user = models.CharField(max_length=50, blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING)


    def __str__(self): return self.type_user

    class Meta:
        managed = False
        db_table = 'user_type'
        verbose_name_plural = 'UserTypes'

class WeekDay(models.Model):
    daywork = models.ForeignKey('DayName', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)

    def __str__(self):
        daynames = str(self.daywork)
        return daynames

    class Meta:
        managed = False
        db_table = 'week_day'
        unique_together = (('daywork', 'company'),)
        verbose_name_plural = 'WeekDays'

class DayName(models.Model):
    dayname = models.IntegerField(blank=True, null=True)

    def __str__(self):
        days = str(self.dayname)
        return days

    class Meta:
        managed = False
        db_table = 'day_name'
        verbose_name_plural = 'DayNames'

