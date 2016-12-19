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
    Company,
    UserCompany,
    WeekDay,
    ScheduleCompany,
    )
from .serializers import (
    # COMPANY
    CompanyCreateUpdateSerializer,
    CompanyDetailSerializer,
    CompanyListSerializer,

    # USERCOMPANY
    UserCompanyCreateUpdateSerializer,
    UserCompanyDetailSerializer,
    UserCompanyListSerializer,

    # WEEKDAY
    WeekDayCreateUpdateSerializer,
    WeekDayListSerializer,

    # SCHEDULECOMPANY
    ScheduleCompanyCreateUpdateSerializer,
    ScheduleCompanyDetailSerializer,
    ScheduleCompanyListSerializer,

    )

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




# USERCOMPANY

class UserCompanyCreateAPIView(CreateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=AuthUser.objects.get(id=self.request.user.id),
            company=Company.objects.get(user=self.request.user.id)
            )


class UserCompanyDetailAPIView(RetrieveAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'first_name'


class UserCompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    lookup_field = 'first_name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(
            user=AuthUser.objects.get(id=self.request.user.id),
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



# DAYWORK OT THE COMPANY

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
