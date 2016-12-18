from rest_framework.serializers import ModelSerializer

from planner_app.models import Company

# COMPANY

class CompanyCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            #'id',
            'name',
            #'owner_company',
            #'active',
        )

class CompanyDetailSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'slug',
            'user',
            'active',
        )


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name',
            'user',
            'active',
        )


# COMPANY
