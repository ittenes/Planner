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


class Client(models.Model):
    name = models.CharField(max_length=250)
    company = models.ForeignKey('Company', models.DO_NOTHING,)


    def __str__(self): return self.name

    class Meta:
        managed = True
        db_table = 'client'


class Company(models.Model):
    name = models.CharField(max_length=75)
    owner_company = models.ForeignKey('AuthUser', models.DO_NOTHING)
    active = models.IntegerField()


    def __str__(self): return self.name

    class Meta:
        managed = True
        db_table = 'company'
        unique_together = (('owner_company', 'name'), ('owner_company', 'active'))


class Planning(models.Model):
    project = models.ForeignKey('Project', models.DO_NOTHING,)
    resource = models.ForeignKey('UserCompany', models.DO_NOTHING, blank=False, null=True)
    week = models.IntegerField(blank=True, null=True)
    dayweek = models.IntegerField()
    hours = models.IntegerField()
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    class Meta:
        managed = True
        db_table = 'planning'



class Project(models.Model):
    client = models.ForeignKey(Client, models.DO_NOTHING,)
    name = models.CharField(max_length=50, blank=True, null=True)
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)


    def __str__(self): return self.name

    class Meta:
        managed = True
        db_table = 'project'
        unique_together = (('name', 'client'),('name', 'company'),)


class Provider(models.Model):
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    cif = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'provider'
        unique_together = (('company', 'cif'),)


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
        managed = True
        db_table = 'request'


class Role(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'role'


class ScheduleCompany(models.Model):
    company_week_day = models.ForeignKey('WeekDay', models.DO_NOTHING)
    hours = models.IntegerField()
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)

    def __str__(self):
        srtday = str(self.company_week_day)
        return srtday

    class Meta:
        managed = True
        db_table = 'schedule_company'
        unique_together = (('company_week_day', 'company'),)


class ScheduleCompanyUser(models.Model):
    user = models.ForeignKey('UserCompany', models.DO_NOTHING, null=True)
    schedule_company = models.ForeignKey(ScheduleCompany, models.DO_NOTHING)
    hour = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'schedule_company_user'
        unique_together = (('user', 'schedule_company'),)



class UserCompany(models.Model):
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)
    type_user = models.ForeignKey('UserType', models.DO_NOTHING,)
    first_name = models.CharField(max_length=50,blank=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    email = models.CharField(max_length=50)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING,blank=True, null=True)


    def __str__(self): return self.first_name

    class Meta:
        managed = True
        db_table = 'user_company'
        unique_together = (('email', 'company'), ('id', 'company'),)



class UserHolidays(models.Model):
    user = models.ForeignKey('UserCompany', models.DO_NOTHING, null=True)
    schedule_company = models.ForeignKey(ScheduleCompany, models.DO_NOTHING)
    hour = models.IntegerField(null=True)
    week = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_holidays'
        unique_together = (('user', 'schedule_company','week'),)



class UserType(models.Model):
    type_user = models.CharField(max_length=50, blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING)


    def __str__(self): return self.type_user

    class Meta:
        managed = True
        db_table = 'user_type'


class WeekDay(models.Model):
    daywork = models.ForeignKey('DayName', models.DO_NOTHING)
    company = models.ForeignKey('Company', models.DO_NOTHING, null=True)

    def __str__(self):
        daynames = str(self.daywork)
        return daynames

    class Meta:
        managed = True
        db_table = 'week_day'
        unique_together = (('daywork', 'company'),)


class DayName(models.Model):
    dayname = models.IntegerField(blank=True, null=True)

    def __str__(self):
        days = str(self.dayname)
        return days

    class Meta:
        managed = True
        db_table = 'day_name'



