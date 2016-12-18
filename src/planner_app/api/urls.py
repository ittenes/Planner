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
    )


urlpatterns = [
    #COMPANY
    url(r'^company/$', CompanyListAPIView.as_view(), name='list'),
    url(r'^company/create/$', CompanyCreateAPIView.as_view(), name='create'),
    url(r'^company/(?P<name>[\w-]+)/$', CompanyDetailAPIView.as_view(), name='detail'),
    url(r'^company/(?P<name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^company/(?P<name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),

    #USERCOMPANY
    url(r'^usercompany/$', UserCompanyListAPIView.as_view(), name='list'),
    url(r'^usercompany/create/$', UserCompanyCreateAPIView.as_view(), name='create'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/$', UserCompanyDetailAPIView.as_view(), name='detail'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^usercompany/(?P<first_name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),
]
