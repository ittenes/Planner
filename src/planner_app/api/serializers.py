from rest_framework.serializers import ModelSerializer

from planner_app.models import (
    Company,
    UserCompany,
    WeekDay,
    ScheduleCompany,
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


# WEEKDAY
class WeekDayCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = WeekDay
        fields = (
            'daywork',
        )

class WeekDayDetailSerializer(ModelSerializer):
    class Meta:
        model = WeekDay
        fields = (
            'daywork',
        )

class WeekDayListSerializer(ModelSerializer):
    class Meta:
        model = WeekDay
        fields = (
            'id',
            'daywork',
            'company',
        )


# SCHEDULECOMPANY
class ScheduleCompanyCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ScheduleCompany
        fields = (
            'company_week_day',
            'hours',
        )

    def __init__(self, *args, **kwargs):
        super(ScheduleCompanyCreateUpdateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user.id
        self.fields['company_week_day'].queryset = WeekDay.objects.filter(
            company=Company.objects.get(user=request_user))

class ScheduleCompanyDetailSerializer(ModelSerializer):
    class Meta:
        model = ScheduleCompany
        fields = (
            'id',
            'company_week_day',
            'hours',
            'company',
        )

class ScheduleCompanyListSerializer(ModelSerializer):
    class Meta:
        model = ScheduleCompany
        fields = (
            'company_week_day',
            'hours',
            'company',
        )
