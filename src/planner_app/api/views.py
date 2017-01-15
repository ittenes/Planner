
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from rest_framework.response import Response
from rest_framework import status

# from rest_framework.filters import(
#     SearchFilter,
#     OrderingFilter,
#     )

from rest_framework.generics import (
    # COMPANY
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from .permissions import IsOwnerOrReadOnly

from planner_app.models import (
    AuthUser,
    Client,
    Company,
    DayName,
    Petition,
    Planning,
    PlanningStatus,
    Project,
    ScheduleCompany,
    ScheduleCompanyUser,
    UserCompany,
    UserHolidays,
    UserType,
    WeekDay,

    )

from .serializers import (
    # CLIENTS
    ClientCreateUpdateSerializer,
    ClientDetailSerializer,
    ClientListSerializer,

    # COMPANY
    CompanyCreateUpdateSerializer,
    CompanyDetailSerializer,
    CompanyListSerializer,

    # PETITION
    PetitionCreateUpdateSerializer,
    PetitionDetailSerializer,
    PetitionListSerializer,

    #PLANNING
    PlanningCreateUpdateSerializer,
    PlanningDetailSerializer,
    PlanningListSerializer,

    # PROJECT
    ProjectCreateUpdateSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,

    # USERCOMPANY
    UserCompanyCreateUpdateSerializer,
    UserCompanyDetailSerializer,
    UserCompanyListSerializer,

    # USERCOMPANY
    UserHolidaysCreateUpdateSerializer,
    UserHolidaysDetailSerializer,
    UserHolidaysListSerializer,

    # SCHEDULECOMPANY
    ScheduleCompanyCreateUpdateSerializer,
    ScheduleCompanyDetailSerializer,
    ScheduleCompanyListSerializer,

    # SCHEDULECOMPANYUSER
    ScheduleCompanyUserCreateUpdateSerializer,
    ScheduleCompanyUserDetailSerializer,
    ScheduleCompanyUserListSerializer,

    # WEEKDAY
    WeekDayCreateUpdateSerializer,
    WeekDayDetailSerializer,
    WeekDayListSerializer,

    )
import django_filters
from rest_framework import viewsets
import rest_framework_filters as filters


import datetime
from collections import Counter
from .planning import ListProjectsPlanning, ListProjectsOkPlanning, HorsProjectsUserPlanning, PlannedOkPlanning

from .invited import InvitationSend

def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError):
        raise Http404




# COMPANY

class CompanyCreateAPIView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=AuthUser.objects.get(id=self.request.user.id), active="1")

        instances = []
        days = DayName.objects.all()
        for day in days:
            instances += [WeekDay(
                daywork=day,
                company=Company.objects.get(user=self.request.user.id),
                active=False)]

        WeekDay.objects.bulk_create(instances)

        user = AuthUser.objects.get(id=self.request.user.id)
        owner = UserCompany(
            company=Company.objects.get(user=self.request.user.id),
            type_user=UserType.objects.get(id=1),
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
            email=self.request.user.email,
            user=user,)
        owner.save()

class CompanyDetailAPIView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'name'

class CompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    lookup_field = 'name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(user=AuthUser.objects.get(id=self.request.user.id), active="1")

class CompanyDeleteAPIView(DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'name'


class CompanyFilter(filters.FilterSet):

    class Meta:
        model = Company

class CompanyListAPIView(ListAPIView):

    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]
    filter_class = CompanyFilter

    def get_queryset(self, *args, **kwargs):
        queryset_list = Company.objects.filter(
            user=self.request.user.id).order_by('name')
        return queryset_list

 # CLIENTS -

class ClientCreateAPIView(CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id), active='1')

class ClientDetailAPIView(RetrieveAPIView):
    serializer_class = ClientDetailSerializer
    lookup_field = 'name'

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        queryset_list = Client.objects.filter(company=mycompany)

        return queryset_list

class ClientUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClientCreateUpdateSerializer
    lookup_field = 'name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        queryset_list = Client.objects.filter(company=mycompany)

        return queryset_list

    def perform_update(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id), active='1')

class ClientDeleteAPIView(DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'name'


def companys(request):
    user = request.user.id

    return user.company_set.all()

class ClientFilter(filters.FilterSet):
    company = filters.RelatedFilter(filterset=CompanyFilter, queryset=Company.objects.all())
    # name = filters.AllLookupsFilter(name='company')
    # company = filters.RelatedFilter('planner_app.views.ClientFilter', name='company', queryset=Client.objects.all())
    class Meta:
        model = Client
        fields = {'company'}


class ClientListAPIView(ListAPIView):
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]
    filter_class = ClientFilter

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        queryset_list = Client.objects.filter(company=mycompany).order_by('name')

        return queryset_list


# PETITION

class PetitionCreateAPIView(CreateAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            company=Company.objects.get(user=self.request.user.id),
            user=AuthUser.objects.get(id=self.request.user.id)
            )


class PetitionDetailAPIView(RetrieveAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionDetailSerializer
    lookup_field = 'id'

class PetitionUpdateAPIView(RetrieveUpdateAPIView):
    #queryset = Petition.objects.all()
    serializer_class = PetitionCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        # saber que semana es hoy
        today = datetime.date.today()
        weekpro = today.isocalendar()[1]
        year = today.isocalendar()[0]
        weeksyear = datetime.date(year, 12, 28).isocalendar()[1]
        queryset_thisyear = Petition.objects.filter(
            company=mycompany,
            week_number__gte=weekpro).order_by('project','week_number',)
        queryset_nextyear = Petition.objects.filter(
            company=mycompany,
            week_number__gte=weekpro).order_by('project','week_number',)

        if queryset_thisyear.exists():
            return queryset_thisyear

        elif queryset_nextyear.exists():
            return queryset_nextyear

        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


    def perform_update(self, serializer):
        instance = serializer.save(
            company=Company.objects.get(user=self.request.user.id),
            user=AuthUser.objects.get(id=self.request.user.id),
            planned=0
            )
        project = instance.project
        week_number = instance.week_number
        year = instance.year

        # borra todas las planis relacionadas
        #busco las planis relacinadas a partir de esta planificacion
        all_petition = []

        all_petition_this_year = Petition.objects.filter(
            project=project,
            week_number__gte=week_number,
            year=year).values_list('id')
        all_petition += all_petition_this_year

        all_petition_next_year = Petition.objects.filter(
            project=project,
            year=year+1).values_list('id')
        all_petition += all_petition_next_year
        # borro todas las plannis del proyecto
        for proj in all_petition:
            peti_proj = Petition.objects.get(pk=proj[0])
            plan_proj = Planning.objects.filter(
                week=peti_proj.week_number,
                project=peti_proj.project,
                resource=peti_proj.resource
                ).values_list('id')

            for id_p in plan_proj:
                PlanningDeleteAPIView().delete(id_p[0])
            # las peticiones las reseteo y pongo como no modificadas
            peti_proj.planned = False
            peti_proj.save()
        instance.save


class PetitionDeleteAPIView(DestroyAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionDetailSerializer
    lookup_field = 'project'

class PetitionListAPIView(ListAPIView):
    #queryset = Petition.objects.all()
    serializer_class = PetitionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        # saber que semana es hoy
        today = datetime.date(2016,12,19)#datetime.date.today()
        weekpro = today.isocalendar()[1]
        year = today.isocalendar()[0]
        weeksyear = datetime.date(year, 12, 28).isocalendar()[1]

        # planifico las planis de esta year mayor o igual que esat semana
        # y les sumo las del year que viene
        queryset_list = Petition.objects.filter(
            company=mycompany,).exclude(
                week_number__lt=weekpro,
                year=year).order_by('project','week_number',)

        return queryset_list


# PLANNING

class PlanningCreateAPIView(CreateAPIView):
    serializer_class = PlanningCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        mycompany = Company.objects.get(user=self.request.user.id)
        # saber que semana es hoy
        today = datetime.date.today()#datetime.date(2016,12,19)#
        weekpro = today.isocalendar()[1]
        year = today.isocalendar()[0]
        weeksyear = datetime.date(year, 12, 28).isocalendar()[1]

        # comienzo a hacer las planificaciones
        listallplanning = ListProjectsPlanning(mycompany).listprojects()
        print('listallplanning:', listallplanning)
        listallplanningok = ListProjectsOkPlanning(listallplanning).listprojectsok()
        print('listallplanningok:', listallplanningok)
        hoursprojectsuser = HorsProjectsUserPlanning(listallplanningok,year,mycompany).horasprojectsuser()

class PlanningDetailAPIView(RetrieveAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningDetailSerializer
    lookup_field = 'id'

class PlanningUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningCreateUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PlanningDeleteAPIView(DestroyAPIView):
    queryset = Planning.objects.all()
    serializer_class = PlanningDetailSerializer
    lookup_field = 'id'

    def get_object(self, id_p):
        try:
            return Planning.objects.get(pk=id_p)

        except Planning.DoesNotExist:
            raise Http404

    def delete(self, id_p):
        self.id_p=id_p
        object = self.get_object(self.id_p)
        object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class PlanningListAPIView(ListAPIView):
    serializer_class = PlanningListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Planning.objects.filter(company=Company.objects.get(user=self.request.user.id))

        return queryset_list



# PROJECT

class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class ProjectDetailAPIView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'slug'

class ProjectUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class ProjectDeleteAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'slug'


class ProjectListAPIView(ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Project.objects.filter(company=Company.objects.get(user=self.request.user.id))
        query = self.request.GET.get("q")

        return queryset_list


# SCHEDULECOMPANY

class ScheduleCompanyCreateAPIView(CreateAPIView):
    queryset = ScheduleCompany.objects.all()
    serializer_class = ScheduleCompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))


class ScheduleCompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ScheduleCompany.objects.all()
    serializer_class = ScheduleCompanyCreateUpdateSerializer
    lookup_field = 'company_week_day'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        instance = serializer.save(company=Company.objects.get(user=self.request.user.id))
        instance.save
        # borro todas las planificiaciones ya que las horas disponibles se han
        # modificado
        today = datetime.date.today()#datetime.date(2016,12,19)#
        weekpro = today.isocalendar()[1]
        year = today.isocalendar()[0]
        weeksyear = datetime.date(year, 12, 28).isocalendar()[1]

        mycompany = Company.objects.get(user=self.request.user.id)
        projects = Project.objects.filter(company=mycompany)
        week_number = weekpro
        year = year

        # borra todas las planis relacionadas
        #busco las planis relacinadas a partir de esta planificacion
        for project in projects:

            all_petition = []

            all_petition_this_year = Petition.objects.filter(
                project=project,
                week_number__gte=week_number,
                year=year).values_list('id')
            all_petition += all_petition_this_year

            all_petition_next_year = Petition.objects.filter(
                project=project,
                year=year+1).values_list('id')
            all_petition += all_petition_next_year
            # borro todas las plannis del proyecto
            for proj in all_petition:
                peti_proj = Petition.objects.get(pk=proj[0])
                plan_proj = Planning.objects.filter(
                    week=peti_proj.week_number,
                    project=peti_proj.project,
                    resource=peti_proj.resource
                    ).values_list('id')

                for id_p in plan_proj:
                    PlanningDeleteAPIView().delete(id_p[0])
                # las peticiones las reseteo y pongo como no modificadas
                peti_proj.planned = False
                peti_proj.planning_status = PlanningStatus.objects.get(id=3)
                peti_proj.save()

        # adapto el horario de los trabajadores a la hora de la empresa
        # siempre que este sea mayor que la hora introducida
        users = UserCompany.objects.filter(company=mycompany)
        for user in users:
            schedule_user = ScheduleCompanyUser.objects.get(user=user, schedule_company=instance.id)
            print('schedule_user', schedule_user.hour)
            print('instance.hours:', instance.hours)
            if schedule_user.hour > instance.hours:
                schedule_user.hour = instance.hours
                schedule_user.save()



class ScheduleCompanyDeleteAPIView(DestroyAPIView):
    queryset = ScheduleCompany.objects.all()
    serializer_class = ScheduleCompanyDetailSerializer
    lookup_field = 'company_week_day'

class ScheduleCompanyListAPIView(ListAPIView):
    serializer_class = ScheduleCompanyListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = ScheduleCompany.objects.filter(
            company=Company.objects.get(user=self.request.user.id))

        return queryset_list


# SCHEDULECOMPANYUSER

class ScheduleCompanyUserCreateAPIView(CreateAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = ScheduleCompanyUserCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

class ScheduleCompanyUserDetailAPIView(RetrieveAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = ScheduleCompanyUserDetailSerializer
    lookup_field = 'user'

class ScheduleCompanyUserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = ScheduleCompanyUserCreateUpdateSerializer
    lookup_field = 'user'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        PetitionDetailAPIView



class ScheduleCompanyUserDeleteAPIView(DestroyAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = ScheduleCompanyUserDetailSerializer
    lookup_field = 'user'

class ScheduleCompanyUserListAPIView(ListAPIView):
    #queryset = ScheduleCompanyUser.objects.all()
    serializer_class = ScheduleCompanyUserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        users = UserCompany.objects.filter(
            company=mycompany).values_list('pk', flat=True)
        queryset_list = ScheduleCompanyUser.objects.filter(user__in=users)
        return queryset_list


# USERCOMPANY and hours work by default

class UserCompanyCreateAPIView(CreateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(company=Company.objects.get(user=self.request.user.id))
        instance.save

        # create de hours by default = hours of the company
        mycompany = Company.objects.get(user=self.request.user.id)
        daysmycoms = ScheduleCompany.objects.filter(company=mycompany).values_list('company_week_day', flat=True)
        user = UserCompany.objects.latest('id')
        instances = [ScheduleCompanyUser(
            user=UserCompany.objects.latest('id'),
            schedule_company=ScheduleCompany.objects.get(company=mycompany, company_week_day=e),
            hour=ScheduleCompany.objects.values_list('hours', flat=True).get(company=mycompany, company_week_day=e),
            )
            for e in daysmycoms
        ]

        ScheduleCompanyUser.objects.bulk_create(instances)

        # send a invitation to register
        if AuthUser.objects.get(email=instance.email):
            user = AuthUser.objects.get(email=instance.email)
            instance.email = user.email
            instance.user = AuthUser.objects.get(email=instance.email)
            instance.save()
        else:
            email = instance.email
            user = self.request.user
            request = self.request
            InvitationSend(user, email, request).invitations()

class UserCompanyDetailAPIView(RetrieveAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'frit_name'

class UserCompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    lookup_field = 'frit_name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))


class UserCompanyDeleteAPIView(DestroyAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'frit_name'

class UserCompanyListAPIView(ListAPIView):
    serializer_class = UserCompanyListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = UserCompany.objects.filter(
            company=Company.objects.get(user=self.request.user.id)
            )
        return queryset_list


# USER HOLIDAYS -

class UserHolidaysCreateAPIView(CreateAPIView):
    queryset = UserHolidays.objects.all()
    serializer_class = UserHolidaysCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

class UserHolidaysDetailAPIView(RetrieveAPIView):
    queryset = UserHolidays.objects.all()
    serializer_class = CompanyDetailSerializer
    lookup_field = 'company_week_day'

class UserHolidaysUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserHolidays.objects.all()
    serializer_class = UserHolidaysCreateUpdateSerializer
    lookup_field = 'company_week_day'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class UserHolidaysDeleteAPIView(DestroyAPIView):
    queryset = UserHolidays.objects.all()
    serializer_class = UserHolidaysDetailSerializer
    lookup_field = 'company_week_day'

class UserHolidaysListAPIView(ListAPIView):
    serializer_class = UserHolidaysDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        users = UserCompany.objects.filter(
            company=mycompany).values_list('pk', flat=True)
        queryset_list = UserHolidays.objects.filter(
            user__in=users).order_by('week')
        return queryset_list


# WORKDAY OT THE COMPANY

class WeekDayCreateAPIView(CreateAPIView):
    queryset = WeekDay.objects.all()
    serializer_class = WeekDayCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class WeekDayUpdateAPIView(RetrieveUpdateAPIView):
    queryset = WeekDay.objects.all()
    serializer_class = WeekDayCreateUpdateSerializer
    lookup_field = 'daywok'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class WeekDayDeleteAPIView(DestroyAPIView):
    queryset = WeekDay.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'daywork'

class WeekDayListAPIView(ListAPIView):
    serializer_class = WeekDayListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = WeekDay.objects.filter(company=Company.objects.get(user=self.request.user.id))

        return queryset_list






#
