from django.conf.urls import url
from django.contrib import admin


from .views import (
    CompanyCreateAPIView,
    CompanyDeleteAPIView,
    CompanyDetailAPIView,
    CompanyListAPIView,
    CompanyUpdateAPIView,
    )


urlpatterns = [
    url(r'^$', CompanyListAPIView.as_view(), name='list'),
    url(r'^create/$', CompanyCreateAPIView.as_view(), name='create'),
    url(r'^(?P<name>[\w-]+)/$', CompanyDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<name>[\w-]+)/edit/$', CompanyUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<name>[\w-]+)/delete/$', CompanyDeleteAPIView.as_view(), name='delete'),

]
