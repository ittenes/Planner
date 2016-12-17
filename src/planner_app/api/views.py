from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    )

from planner_app.models import Company
from .serializers import (
    CompanyCreateSerializer,
    CompanyDetailSerializer,
    CompanyListSerializer,
    )

class CompanyCreateAPIView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer


class CompanyDetailAPIView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'name'


class CompanyUpdateAPIView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'name'


class CompanyDeleteAPIView(DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'name'


class CompanyListAPIView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer

