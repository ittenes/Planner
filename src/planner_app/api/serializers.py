from rest_framework.serializers import ModelSerializer

from planner_app.models import (
    Company,
    UserCompany,
    )

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



# USERCOMPANY
class UserCompanyCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
            'email',
            'first_name',
            'last_name',
            'type_user',
        )

class UserCompanyDetailSerializer(ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
            'id',
            'company',
            'slug',
            'type_user',
            'first_name',
            'last_name',
            'email',
            'user',
        )


class UserCompanyListSerializer(ModelSerializer):
    class Meta:
        model = UserCompany
        fields = (
            'company',
            'slug',
            'type_user',
            'first_name',
            'last_name',
            'email',
            'user',
        )
