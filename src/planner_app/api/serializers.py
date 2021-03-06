from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )

import datetime

from planner_app.models import (
    AuthUser,
    Client,
    Company,
    Petition,
    Planning,
    PlanningStatus,
    Project,
    ProjectStatus,
    UserCompany,
    WeekDay,
    ScheduleCompany,
    ScheduleCompanyUser,
    UserHolidays,
    )
import django_filters
# CLIENTS

class ClientCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = (
            #'id',
            'name',
            #'user',
            #'active',
            #'slug'
        )

class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'company',
            'active',
            'slug'
        )

class ClientListSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'name',
            'company',
            'active',
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
            'slug',
        )


# PETITION

class PetitionCreateUpdateSerializer(ModelSerializer):
    #week_number = SerializerMethodField()

    class Meta:
        model = Petition
        fields = (
            #'id',
            #'company',
            'project',
            'resource',
            'time',
            'day_week_in',
            'day_week_out',
            'week_number',
            'year',
            'planning_status',
            #'planned',
        )


    def __init__(self, *args, **kwargs):
        super(PetitionCreateUpdateSerializer, self).__init__(*args, **kwargs)
        # only show the resources of de user company
        request_user = self.context['request'].user.id
        mycompany = Company.objects.filter(user=request_user).values_list('id', flat=True)
        self.fields['project'].queryset = Project.objects.filter(company=mycompany)
        self.fields['resource'].queryset = UserCompany.objects.filter(company=mycompany, active=1)
        self.fields['day_week_in'].queryset = WeekDay.objects.filter(company=mycompany)
        self.fields['day_week_out'].queryset = WeekDay.objects.filter(company=mycompany)
        self.fields['planning_status'].queryset = PlanningStatus.objects.all()


class PetitionDetailSerializer(ModelSerializer):

    class Meta:
        model = Petition
        fields = (
            'id',
            'company',
            'project',
            'resource',
            'time',
            'day_week_in',
            'day_week_out',
            'week_number',
            'planned',
            'planning_status',
        )

class PetitionListSerializer(ModelSerializer):

    class Meta:
        model = Petition
        fields = (
            #'id',
            'company',
            'project',
            'resource',
            'time',
            'day_week_in',
            'day_week_out',
            'week_number',
            'planned',
        )


 # PLANNING

class PlanningCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Planning
        fields = (
            # #'id',
            # 'project',
            # 'resource',
            # 'week',
            # 'dayweek',
            # 'hours',
            # 'company',

        )

class PlanningDetailSerializer(ModelSerializer):

    class Meta:
        model = Planning
        fields = (
            'id',
            'project',
            'resource',
            'week',
            'dayweek',
            'hours',
            'company',
            'planning_status',
        )

class PlanningListSerializer(ModelSerializer):

    class Meta:
        model = Planning
        fields = (
            #'id',
            'project',
            'resource',
            'week',
            'dayweek',
            'hours',
            'company',
            'planning_status',
        )


# PROJECT

class ProjectCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = (
            #'id',
            'name',
            'client',
            #'company',
            #'slug',
            'status',
            )

    def __init__(self, *args, **kwargs):
        super(ProjectCreateUpdateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user.id
        self.fields['client'].queryset = Client.objects.filter(
            company=Company.objects.get(user=request_user))
        self.fields['status'].queryset = ProjectStatus.objects.all()


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'client',
            'company',
            'slug',
            'status',
        )

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        #depth = 1
        fields = (
            #'id',
            'name',
            'client',
            'company',
            #'slug',
            'status',
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
            'id',
            'company_week_day',
            'hours',
            'company',
        )


# SCHEDULECOMPANYUSER

class ScheduleCompanyUserCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = ScheduleCompanyUser
        fields = (
            'user',
            'schedule_company',
            'hour',
        )

    def __init__(self, *args, **kwargs):
        super(ScheduleCompanyUserCreateUpdateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user.id
        self.fields['user'].queryset = UserCompany.objects.filter(
            company=Company.objects.get(user=request_user))
        self.fields['schedule_company'].queryset = ScheduleCompany.objects.filter(
            company=Company.objects.get(user=request_user))


class ScheduleCompanyUserDetailSerializer(ModelSerializer):

    class Meta:
        model = ScheduleCompanyUser
        fields = (
            'id',
            'user',
            'schedule_company',
            'hour',
        )

class ScheduleCompanyUserListSerializer(ModelSerializer):

    class Meta:
        model = ScheduleCompanyUser
        fields = (
            'id',
            'user',
            'schedule_company',
            'hour',
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
            'active',
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
            'active',
        )


# USERHOLIDAYS

class UserHolidaysCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = UserHolidays
        fields = (
            #'id',
            'user',
            'week',
            'schedule_company',
            'hour',

            )

    def __init__(self, *args, **kwargs):
        super(UserHolidaysCreateUpdateSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user.id
        self.fields['user'].queryset= UserCompany.objects.filter(company=Company.objects.get(user=request_user))
        print (request_user)

        mycompany = Company.objects.filter(user=request_user).values_list('id', flat=True)
        print (mycompany)
        daysmycompany = ScheduleCompany.objects.filter(
            company__in=mycompany).values_list('company_week_day', flat=True)
        print (daysmycompany)
        self.fields['schedule_company'].queryset = ScheduleCompany.objects.filter(company__in=mycompany)

        # calculate how many week there are from now to year end
        today = datetime.date.today()
        print (today)
        weeknow = today.isocalendar()[1]
        year = today.isocalendar()[0]
        print (weeknow)
        print (year)
        weeklast = datetime.date(year, 12, 31).isocalendar()[1]
        print (weeklast)
        keyallweeks = list(range(weeknow + 1, weeklast))
        valueallweeks = list(range(weeknow + 1, weeklast))
        twotuple = []
        for keyallweek, valueallweek in zip(keyallweeks, valueallweeks):
            if weeklast >= 0:
                twotuple += [(keyallweek, valueallweek)]

        # mirar como mostrar las semanas no se si son necesarias
        # IMPARTANTE: PARA LA ENTRADA DE DATOS NO HACE FALTA QUE HAYA NADA MAS
        # COMO MUCHO COMPROBAR QUE LAS SEMANAS SEAN LAS QUE CORRESPONDE
        #self.fields['week'] = twotuple

class UserHolidaysDetailSerializer(ModelSerializer):

    class Meta:
        model = UserHolidays
        fields = (
            'id',
            'schedule_company',
            'user',
            'hour',
            'week',
        )

class UserHolidaysListSerializer(ModelSerializer):

    class Meta:
        model = UserHolidays
        fields = (
            #'id',
            'schedule_company',
            'user',
            'hour',
            'week',
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
