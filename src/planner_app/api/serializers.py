from rest_framework.serializers import ModelSerializer

from planner_app.models import Company


class CompanyCreateSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            #'id',
            'name',
            'owner_company',
            #'active',
        )

class CompanyDetailSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'owner_company',
            'active',
        )


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'owner_company',
            'active',
        )


