from django.conf.urls import url
from django.contrib import admin


from .views import (
    # CLIENT
    ClientCreateAPIView,
    ClientDeleteAPIView,
    ClientDetailAPIView,
    ClientListAPIView,
    ClientUpdateAPIView,

    # COMPANY
    CompanyCreateAPIView,
    CompanyDeleteAPIView,
    CompanyDetailAPIView,
    CompanyListAPIView,
    CompanyUpdateAPIView,

    # PETITION
    PetitionCreateAPIView,
    PetitionDeleteAPIView,
    PetitionDetailAPIView,
    PetitionListAPIView,
    PetitionUpdateAPIView,

    # PROJECTS
    ProjectCreateAPIView,
    ProjectDeleteAPIView,
    ProjectDetailAPIView,
    ProjectListAPIView,
    ProjectUpdateAPIView,

    # USERCOMPANY
    UserCompanyCreateAPIView,
    UserCompanyDeleteAPIView,
    UserCompanyDetailAPIView,
    UserCompanyListAPIView,
    UserCompanyUpdateAPIView,

    # USERHOLIDAYS
    UserHolidaysCreateAPIView,
    UserHolidaysDeleteAPIView,
    UserHolidaysDetailAPIView,
    UserHolidaysListAPIView,
    UserHolidaysUpdateAPIView,

    # SCHEDULECOMPANY
    ScheduleCompanyCreateAPIView,
    ScheduleCompanyDeleteAPIView,
    ScheduleCompanyListAPIView,
    ScheduleCompanyUpdateAPIView,

    # SCHEDULECOMPANY
    ScheduleCompanyUserCreateAPIView,
    ScheduleCompanyUserDeleteAPIView,
    ScheduleCompanyUserDetailAPIView,
    ScheduleCompanyUserListAPIView,
    ScheduleCompanyUserUpdateAPIView,

    # WEEKDAY
    WeekDayCreateAPIView,
    WeekDayDeleteAPIView,
    WeekDayListAPIView,
    WeekDayUpdateAPIView,

    )


urlpatterns = [
    # CLIENTS
    url(r'^client/$', ClientListAPIView.as_view(), name='list'),
    url(r'^client/create/$', ClientCreateAPIView.as_view(), name='create'),
    url(r'^client/(?P<name>[\w-]+)/$', ClientDetailAPIView.as_view(), name='detail'),
    url(r'^client/(?P<name>[\w-]+)/edit/$', ClientUpdateAPIView.as_view(), name='update'),
    url(r'^client/(?P<name>[\w-]+)/delete/$', ClientDeleteAPIView.as_view(), name='delete'),

    # COMPANY
    url(r'^company/$', CompanyListAPIView.as_view(), name='list'),
    url(r'^company/create/$', CompanyCreateAPIView.as_view(), name='create'),
    url(r'^company/(?P<name>[\w-]+)/$', CompanyDetailAPIView.as_view(), name='detail'),
    url(r'^company/(?P<name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^company/(?P<name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),

    # PETITION
    url(r'^petition/$', PetitionListAPIView.as_view(), name='list'),
    url(r'^petition/create/$', PetitionCreateAPIView.as_view(), name='create'),
    url(r'^petition/(?P<project>[\w-]+)/$', PetitionDetailAPIView.as_view(), name='detail'),
    url(r'^petition/(?P<project>[\w-]+)/edit/$', PetitionUpdateAPIView.as_view(), name='update'),
    url(r'^petition/(?P<project>[\w-]+)/delete/$', PetitionDeleteAPIView.as_view(), name='delete'),

    # PROJECT
    url(r'^project/$', ProjectListAPIView.as_view(), name='list'),
    url(r'^project/create/$', ProjectCreateAPIView.as_view(), name='create'),
    url(r'^project/(?P<name>[\w-]+)/$', ProjectDetailAPIView.as_view(), name='detail'),
    url(r'^project/(?P<name>[\w-]+)/edit/$', ProjectUpdateAPIView.as_view(), name='update'),
    url(r'^project/(?P<name>[\w-]+)/delete/$', ProjectDeleteAPIView.as_view(), name='delete'),

    # SCHEDULECOMPANY
    url(r'^schedulecompany/$', ScheduleCompanyListAPIView.as_view(), name='list'),
    url(r'^schedulecompany/create/$', ScheduleCompanyCreateAPIView.as_view(), name='create'),
    url(r'^schedulecompany/(?P<company_week_day>[\w-]+)/edit/$', ScheduleCompanyUpdateAPIView.as_view(), name='update'),
    url(r'^schedulecompany/(?P<company_week_day>[\w-]+)/delete/$', ScheduleCompanyDeleteAPIView.as_view(), name='delete'),

    # SCHEDULECOMPANYUSER
    url(r'^schedulecompanyuser/$', ScheduleCompanyUserListAPIView.as_view(), name='list'),
    url(r'^schedulecompanyuser/create/$', ScheduleCompanyUserCreateAPIView.as_view(), name='create'),
    url(r'^schedulecompanyuser/(?P<user>[\[0-9]+)/$',ScheduleCompanyUserDetailAPIView.as_view(), name='detail'),
    url(r'^schedulecompanyuser/(?P<user>[\w-]+)/edit/$', ScheduleCompanyUserUpdateAPIView.as_view(), name='update'),
    url(r'^schedulecompanyuser/(?P<user>[\w-]+)/delete/$', ScheduleCompanyUserDeleteAPIView.as_view(), name='delete'),

    # USERHOLIDAYS
    url(r'^userholidays/$', UserHolidaysListAPIView.as_view(), name='list'),
    url(r'^userholidays/create/$', UserHolidaysCreateAPIView.as_view(), name='create'),
    url(r'^userholidays/(?P<user>[\[0-9]+)/$', UserHolidaysDetailAPIView.as_view(), name='detail'),
    url(r'^userholidays/(?P<user>[\w-]+)/edit/$', UserHolidaysUpdateAPIView.as_view(), name='update'),
    url(r'^userholidays/(?P<user>[\w-]+)/delete/$', UserHolidaysDeleteAPIView.as_view(), name='delete'),

    # USERCOMPANY
    url(r'^usercompany/$', UserCompanyListAPIView.as_view(), name='list'),
    url(r'^usercompany/create/$', UserCompanyCreateAPIView.as_view(), name='create'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/$', UserCompanyDetailAPIView.as_view(), name='detail'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),

    # WEEKDAY
    url(r'^weekday/$', WeekDayListAPIView.as_view(), name='list'),
    url(r'^weekday/create/$', WeekDayCreateAPIView.as_view(), name='create'),
    url(r'^weekday/(?P<daywork>[\w-]+)/edit/$', WeekDayUpdateAPIView.as_view(), name='update'),
    url(r'^weekday/(?P<daywork>[\w-]+)/delete/$', WeekDayDeleteAPIView.as_view(), name='delete'),


]
