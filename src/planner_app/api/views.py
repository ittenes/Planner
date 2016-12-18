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

from planner_app.models import Company, AuthUser

from .serializers import (
    # COMPANY
    CompanyCreateUpdateSerializer,
    CompanyDetailSerializer,
    CompanyListSerializer,
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
