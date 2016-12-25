from django.conf.urls import include, url

from . import views

from django.views.generic import TemplateView

urlpatterns = [
    #INICIO
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    # USER COMPANY
    url(r'^usercompany/list/', views.user_company_list, name='usercompanylist'),
    url(r'^usercompany/new/$', views.myusercompany, name='usercompanynew'),

    # COMPANY
    url(r'^company/new/$', views.companynew, name='companynew'),
    url(r'^company/list/', views.company_list, name='companylist'),

    # CLIENTS
    url(r'^clients/new/', views.clientsnew, name='clients'),
    url(r'^clients/list/', views.clients_list, name='clientslist'),

    # PROYECTS
    url(r'^prjects/new/', views.projectsnew, name='projects'),
    url(r'^prjects/list/', views.projects_list, name='projectslist'),

    # DAYWORKS
    url(r'^weekday/new/', views.weekdaynew, name='weekday'),
    url(r'^weekday/list/', views.weekday_list, name='weekdaylist'),

    # COMPANY SCHEDULE
    url(r'^schedulecompany/new/', views.schedulecompanynew, name='schedulecompany'),
    url(r'^schedulecompany/list/', views.schedulecompany_list, name='schedulecompanylist'),

    # REQUEST
    url(r'^petition/new/', views.petitionnew, name='petition'),
    url(r'^petition/list/', views.petition_list, name='petitionlist'),

    # HOLIDAYS
    url(r'^holiday/new/', views.userholidaysnew, name='holiday'),
    url(r'^holiday/list/', views.userholidays_list, name='holidaylist'),

    # PLANNER
    url(r'^planning/list/', views.planning, name='nameprolist'),
]
