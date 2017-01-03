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

import datetime
from collections import Counter

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

class PlanningCreateAPIView(CreateAPIView):
    serializer_class = PlanningCreateUpdateSerializer
    permission_classes = [IsAuthenticated]



    def perform_create(self, serializer):

        mycompany = Company.objects.get(user=self.request.user.id)
        # saber que semana es hoy
        today = datetime.date(2016,12,19)#datetime.date.today()
        weekpro = today.isocalendar()[1]
        year = today.isocalendar()[0]
        weeksyear = datetime.date(year, 12, 28).isocalendar()[1]
        print('year', year)
        print('weeksyear', weeksyear)
        print('today', today)
        print('weekpro', weekpro)
        # lista de la peticiones por proyectos
        nameprolist = Petition.objects.filter(
            company=mycompany, planned=0).values_list('project')
        print('nameprolist', nameprolist)
        #cuento los repetidos

        repitpro = Counter(nameprolist)

        print('repitpro', repitpro)

        #como Counter me devuelve los proyectos en orden por el numero de
        #repeticiones que hay lo que hago es generar un alista en base a esos
        # listtotal estan todos los proyectos ordenado por nuero de repeticiones
        # que aparcen

        def project_repit():
            listall = []
            for key, count in repitpro.most_common():
                listallpro = Petition.objects.filter(
                    company=mycompany, project=key, ).values_list('project')
                listall += [(listallpro)]
            print ('primera muestra', listall)

            return listall

        #listado de proyectos por ordenados por el numero repeticiones
        listtotal = project_repit()
        print('listtotal', listtotal)



        def crate_plannig(repitpro):
        # agrupo todas las planificaciones hechas de esos proyectos
            print ('variables de proyectos', repitpro)
            profirst = []
            for key, count in repitpro.most_common():
                reqtoplann = Petition.objects.filter(project=key).order_by(
                    'week_number', 'resource').values_list('pk')
                profirst += [(reqtoplann)]
            print ('bruto de lista', profirst)
            # ahora la tupla lo convierto en una lista, y tengo el listado de todas
            # las planis que tengo que ir metiendo porque viene de la semana que anterior
            # profirst_list = [list(i) for i in profirst]
            profirst_list = []
            # itero la lista para poder sacar los proyectos
            for i in profirst:
                for e in i:
                    profirst_list += e
            print ('listado de proyectos', profirst_list)

            # los proyectos que no se pueden planificar los saco a una lista

            # programo cada proyecto de la lista creada
            mycompany = Company.objects.get(user=self.request.user.id)

            print ('mycompany', mycompany)

            for prog in profirst_list:
                print ('proyecto id del for', prog)
                # identifico el proyecto
                prog_rec = Petition.objects.get(pk=prog)
                print('proyecto_id', prog_rec)
                print('user',prog_rec.resource_id)
                # miro si el proyecto esta ya planificado para sacarlo del loop

                if prog_rec.planned == False :
                    # miro los dias que el proyecto tiene establcidos de trabajo
                    listdays = range(prog_rec.day_week_in, prog_rec.day_week_out + 1)
                    print ('dias establecidos de trabajo', listdays)

                    # miro las horas que trabaja el usuario en esos dias y si tiene
                    # vacaciones
                    # saco las hora disponibles al dia del usuario diccionario (dia:hora)
                    listhoursuser_t = []
                    for listday in listdays:
                        hoursuser = ScheduleCompanyUser.objects.get(
                            user=prog_rec.resource_id,
                            schedule_company=ScheduleCompany.objects.get(company=mycompany,
                                company_week_day=WeekDay.objects.get(company=mycompany, daywork=listday))
                            )
                        listhoursuser_t += [(listday, hoursuser.hour)]
                    print ('horario de usaurio', listhoursuser_t)

                    # saco las horas que tiene de vacaciones el usuaario en un dicionario
                    # (dia:hora)
                    listhoursholliday_t = []
                    for listday in listdays:
                        try:
                            hoursuser_holliday = UserHolidays.objects.get(
                                user=prog_rec.resource,
                                schedule_company=listday,
                                week=prog_rec.week_number
                                )
                            listhoursholliday_t += [(listday, hoursuser_holliday.hour)]
                        except UserHolidays.DoesNotExist:
                            listhoursholliday_t += [(listday, 0)]
                    print ('horas vacaciones', listhoursholliday_t)

                    # saco las horas que tiene en esa semana ya planificadas en un
                    # dicionario (dia:hora)
                    weektest = prog_rec.week_number
                    print('weektest',weektest)

                    listnowplann_t = []
                    for listday in listdays:
                        try:
                            print ('llego hasta aqui')
                            houruser_plann = Planning.objects.get(
                                resource=prog_rec.resource_id,
                                dayweek=listday,
                                week=prog_rec.week_number,
                                year=year)
                            print ('mirar', houruser_plann)
                            listnowplann_t += [(listday, houruser_plann.hours)]
                        except Planning.DoesNotExist:
                            listnowplann_t += [(listday, 0)]
                    print ('horas disponibles: '), (listnowplann_t)

                    # =========================================================================
                    # >>>>>>>>>>>>> da como resultado los elmetnos que no son iguales
                    # hworkandhholliday = len(
                    #    set(listhoursuser_t).intersection(listhoursholliday_t))
                    # =========================================================================

                    # estas son las hoars que dispone el recurso para ser planificado en
                    # este proyecto
                    real_hours_resource = list(set(listhoursuser_t) -
                                               set(listhoursholliday_t) -
                                               set(listnowplann_t))
                    print ('horas reales de usuario', real_hours_resource)

                    # hay que ver si las horas disponibles son menos que las horas del
                    # proyecto
                    listhours = ()
                    for d in real_hours_resource:
                        listhours += d[1:]

                    total_listhours = sum(listhours)

                    print ('horas disponibles del usuario', total_listhours)
                    print ('horas del proyecto', prog_rec.time)

                    real_hours_resource_ord = sorted(real_hours_resource)
                    print (real_hours_resource_ord)

                    # si las horas del proyecto son igual o menor que
                    # las disponibles lo planifico
                    if prog_rec.time <= total_listhours:

                        print('lo planifico')
                        instances = []
                        hoursneed = prog_rec.time

                        # voy restando las horas a las horas del proyecto
                        for plan in real_hours_resource_ord:
                            print(hoursneed)
                            if plan[1] <= hoursneed:
                                hoursneed -= plan[1]
                                instances += [Planning(
                                    project=prog_rec.project,
                                    resource=prog_rec.resource,
                                    week=prog_rec.week_number,
                                    dayweek=plan[0],
                                    hours=plan[1],
                                    company=prog_rec.company,
                                    year=prog_rec.year)]

                            # si las horas restadas son menos que las
                            # horas que hay en el dia pongo las horas que restan
                            elif hoursneed != 0:
                                instances += [Planning(
                                    project=prog_rec.project,
                                    resource=prog_rec.resource,
                                    week=prog_rec.week_number,
                                    dayweek=plan[0],
                                    hours=hoursneed,
                                    company=prog_rec.company,
                                    year=prog_rec.year)]
                                hoursneed -= hoursneed
                            else:
                                pass

                        prog_rec.planned = True
                        prog_rec.save()
                        Planning.objects.bulk_create(instances)
                        print('planifico', prog_rec.week_number )



            # '''ESTA PARTE HAY QUE MIRAR SI SE EJECUTA AQUI HAY QUE HACER LISTA DE
            # PLANIFICADOS Y NO PLANIFICADOS -  ESTA LISTA DE DEVUELVE LOS PROYECTOS QUE
            # NO SE HAN PODIDO PLANIFICAR'''
            #
            #         elif prog_rec.time > total_listhours or real_hours_resource == False:
            #             # los proyectos que no tiene horas suficientes pasan a
            #             # una lista de no planificados
            #             no_plannig = prog_rec.id
            #             list_no_plannig.append(no_plannig)
            #             print('no lo planifico', no_plannig)
            #
            #         else:
            #             pass
            #
            #             print('no lo planifico')
            #
            #     else:
            #         pass



        '''HASTA AQUI'''
        crate_plannig(repitpro)
    #     # Creo las planificaciones primero las repetidas despues en orden decreciente de alcance
    #     print('start semana anterior ===============')
    #     crate_plannig(listrepit)
    #     print('end semana anterior ===============')
    #     print(' 3 start semanas ================== ')
    #     crate_plannig(listtothree)
    #     print(' 3 end semanas ================== ')
    #     print(' 2 start semanas ================== ')
    #     crate_plannig(listtotwo)
    #     print(' 2 end semanas ================== ')
    #     print(' 1 start semanas ================== ')
    #     crate_plannig(listtoone)
    #     print(' 1 end semanas ================== ')
    #
    #     print ('list_no_plannig',list_no_plannig)
    # # =========================================================================
    #     # se ve en pantalla
    #     # lista todos las peticiones de recurso que hay


''' METIDO EN EL ANTERIOR COMENTARIO'''
        # myuser = request.user.id
        # nameprolist = Petition.objects.filter(id__in=list_no_plannig).order_by(
        #     'week_number', 'resource', 'project')

''' HASTA AQUI'''


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
    queryset = UserCompany.objects.all()
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
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'frit_name'


class UserCompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyCreateUpdateSerializer
    lookup_field = 'frit_name'
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(
            company=Company.objects.get(user=self.request.user.id)
            )

class UserCompanyDeleteAPIView(DestroyAPIView):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanyDetailSerializer
    lookup_field = 'frit_name'


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
