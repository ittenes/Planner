from django.conf.urls import url
from django.contrib import admin


from .views import (
    #COMPANY
    CompanyCreateAPIView,
    CompanyDeleteAPIView,
    CompanyDetailAPIView,
    CompanyListAPIView,
    CompanyUpdateAPIView,

    #USERCOMPANY
    UserCompanyCreateAPIView,
    UserCompanyDeleteAPIView,
    UserCompanyDetailAPIView,
    UserCompanyListAPIView,
    UserCompanyUpdateAPIView,

    #WEEKDAY
    WeekDayCreateAPIView,
    WeekDayDeleteAPIView,
    WeekDayListAPIView,
    WeekDayUpdateAPIView,

    #SCHEDULECOMPANY
    ScheduleCompanyCreateAPIView,
    ScheduleCompanyDeleteAPIView,
    ScheduleCompanyListAPIView,
    ScheduleCompanyUpdateAPIView,
    )


urlpatterns = [
    # COMPANY
    url(r'^company/$', CompanyListAPIView.as_view(), name='list'),
    url(r'^company/create/$', CompanyCreateAPIView.as_view(), name='create'),
    url(r'^company/(?P<name>[\w-]+)/$', CompanyDetailAPIView.as_view(), name='detail'),
    url(r'^company/(?P<name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^company/(?P<name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),

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

    # SCHEDULECOMPANY
    url(r'^schedulecompany/$', ScheduleCompanyListAPIView.as_view(), name='list'),
    url(r'^schedulecompany/create/$', ScheduleCompanyCreateAPIView.as_view(), name='create'),
    url(r'^schedulecompany/(?P<company_week_day>[\w-]+)/edit/$', ScheduleCompanyUpdateAPIView.as_view(), name='update'),
    url(r'^schedulecompany/(?P<company_week_day>[\w-]+)/delete/$', ScheduleCompanyDeleteAPIView.as_view(), name='delete'),


]
