import django_filters
from rest_framework import viewsets
import rest_framework_filters as filters

from planner_app.models import Company

# def companys(request):
#     user = request.user
#     return user.company_set.all()


class CompanyFilter(filters.FilterSet):

    class Meta:
        model = Company
        fields = ('name')
