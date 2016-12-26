from django.db.models import Q

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
    Petition,
    Planning,
    Project,
    ScheduleCompany,
    ScheduleCompanyUser,
    UserCompany,
    UserHolidays,
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

    # PLANNING
    # PlannigCreateUpdateSerializer,
    # PlannigDetailSerializer,
    # PlannigListSerializer,

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
        queryset_list = Client.objects.filter(
            company=mycompany)
        return queryset_list

class ClientUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = ClientCreateUpdateSerializer
    lookup_field = 'name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        queryset_list = Client.objects.filter(
            company=mycompany)
        return queryset_list

    def perform_update(self,serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id), active='1')

class ClientDeleteAPIView(DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    lookup_field = 'name'

class ClientListAPIView(ListAPIView):
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        mycompany = Company.objects.get(user=self.request.user.id)
        queryset_list = Client.objects.filter(
            company=mycompany).order_by('name')
        return queryset_list


# COMPANY

class CompanyCreateAPIView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=AuthUser.objects.get(id=self.request.user.id), active="1")

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

class CompanyListAPIView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]


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
    lookup_field = 'project'

class PetitionUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionCreateUpdateSerializer
    lookup_field = 'project'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            company=Company.objects.get(user=self.request.user.id),
            user=AuthUser.objects.get(id=self.request.user.id)
            )

class PetitionDeleteAPIView(DestroyAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionDetailSerializer
    lookup_field = 'project'

class PetitionListAPIView(ListAPIView):
    queryset = Petition.objects.all()
    serializer_class = PetitionListSerializer
    permission_classes = [IsAuthenticated]


# PLANNING

# class PlanningCreateAPIView(CreateAPIView):
#     queryset = Planning.objects.all()
#     serializer_class = PlanningCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(
#             company=Company.objects.get(user=self.request.user.id),
#             user=AuthUser.objects.get(id=self.request.user.id)
#             )
#
# class PlanningDetailAPIView(RetrieveAPIView):
#     queryset = Planning.objects.all()
#     serializer_class = PlanningDetailSerializer
#     lookup_field = 'project'
#
# class PlanningUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Planning.objects.all()
#     serializer_class = PlanningCreateUpdateSerializer
#     lookup_field = 'project'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(
#             company=Company.objects.get(user=self.request.user.id),
#             user=AuthUser.objects.get(id=self.request.user.id)
#             )
#
# class PlanningDeleteAPIView(DestroyAPIView):
#     queryset = Planning.objects.all()
#     serializer_class = PlanningDetailSerializer
#     lookup_field = 'project'
#
# class PlanningListAPIView(ListAPIView):
#     queryset = Planning.objects.all()
#     serializer_class = PlanningListSerializer
#     permission_classes = [IsAuthenticated]
#


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
    lookup_field = 'name'

class ProjectUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateUpdateSerializer
    lookup_field = 'name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class ProjectDeleteAPIView(DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'name'

class ProjectListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]


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
        serializer.save(company=Company.objects.get(user=self.request.user.id))

class ScheduleCompanyDeleteAPIView(DestroyAPIView):
    queryset = ScheduleCompany.objects.all()
    serializer_class = ScheduleCompanyDetailSerializer
    lookup_field = 'company_week_day'

class ScheduleCompanyListAPIView(ListAPIView):
    serializer_class = ScheduleCompanyListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = ScheduleCompany.objects.filter(company=Company.objects.get(user=self.request.user.id))
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
        queryset_list = ScheduleCompanyUser.objects.filter(
            user__in=users)
        return queryset_list


# USERCOMPANY and hours work by default

class UserCompanyCreateAPIView(CreateAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=Company.objects.get(user=self.request.user.id))
        # create de hours by default = of the company hours
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


class UserCompanyDetailAPIView(RetrieveAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'first_name'


class UserCompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ScheduleCompanyUser.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    lookup_field = 'first_name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(
            company=Company.objects.get(user=self.request.user.id)
            )

class UserCompanyDeleteAPIView(DestroyAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'first_name'


class UserCompanyListAPIView(ListAPIView):
    serializer_class = UserCompanyListSerializer
    permission_classes = [IsAuthenticated]
    # mira los filtros da un error pero hay que ver si hay installar
    # una aplicacion especifica
    # filter_backends = [SearchFilter, OrderingFilter]
    # search_fields = ['first_name','last_name','type_user']


    def get_queryset(self, *args, **kwargs):
        queryset_list = UserCompany.objects.filter(
            company=Company.objects.get(user=self.request.user.id)
            )
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(first_name__icontains=query)|
                Q(last_name__icontains=query)|
                Q(type_user__icontains=query)
                ).distinct()
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
