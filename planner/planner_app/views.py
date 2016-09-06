from django.shortcuts import render
from django.shortcuts import redirect
import datetime
# Create your views here.

from .models import UserCompany
from .models import UserType
from .models import AuthUser, Company
from .models import Client
from .models import Project
from .models import WeekDay
from .models import ScheduleCompany
from .models import Request
from .models import UserHolidays
from .models import ScheduleCompanyUser
from .models import Planning

from .forms import UserCompanyForm
from .forms import NewUserCompanyForm
from .forms import MyUserCompanyForm
from .forms import CompanyForm
from .forms import ClientForm
from .forms import ProjectForm
from .forms import WeekDayForm
from .forms import ScheduleCompanyForm
from .forms import RequestForm
from .forms import UserHolidaysForm
from .forms import ScheduleCompanyUserForm

# USER COMPANY AND DEFAULT USER SCHEDULE
# users list


def user_company_list(request):
    myuser = Company.objects.get(owner_company=request.user.id)
    usercompanys = UserCompany.objects.filter(company=myuser).order_by()
    return render(request, 'usercompanylist.html',
                  {'usercompanys': usercompanys})

# users create anda crate de default user schedule


def myusercompany(request):
    if request.method == "POST":

        # variables
        mycompany = Company.objects.get(owner_company=request.user.id)
        print(mycompany)
        daysmycoms = ScheduleCompany.objects.filter(
            company=mycompany).values_list('company_week_day', flat=True)
        print(daysmycoms)
        user = UserCompany.objects.latest('id')
        print(user)

        # formularios
        myusercompanyform = MyUserCompanyForm(request.POST)

        if myusercompanyform.is_valid():
            myuserform = myusercompanyform.save(commit=False)
            myuserform.company = Company.objects.get(
                owner_company=request.user.id)
            myuserform.user = AuthUser.objects.get(id=request.user.id)
            myuserform.save()

            instances = [ScheduleCompanyUser(
                user=UserCompany.objects.latest('id'),
                schedule_company=ScheduleCompany.objects.get(
                    company=mycompany, company_week_day=e),
                hour=ScheduleCompany.objects.values_list('hours', flat=True).get(
                    company=mycompany, company_week_day=e),
            )
                for e in daysmycoms
            ]

            ScheduleCompanyUser.objects.bulk_create(instances)

            return redirect('views.user_company_list',)

    else:
        myusercompanyform = MyUserCompanyForm()
    return render(request, 'usercompanynew.html', {'myusercompanyform': myusercompanyform})


# COMPANY
# company list

def company_list(request):
    companys = Company.objects.filter().order_by()
    return render(request, 'companylist.html', {'companys': companys})

# CREATE COMPANY and USER OWNER OF THE COMAPANY


def companynew(request):

    if request.method == "POST":
        form_company = CompanyForm(request.POST)
        form_usercompanyactive = UserCompanyForm(request.POST)
        print('hola')
        if form_company.is_valid() and form_usercompanyactive.is_valid():
            company = form_company.save(commit=False)
            company.owner_company = AuthUser.objects.get(id=request.user.id)
            company.active = "1"
            company.save()
            # when creta the new company save de user in de user_company how
            #    owner of the company
            usercompany = form_usercompanyactive.save(commit=False)
            usercompany.company = Company.objects.get(
                owner_company=request.user.id)
            usercompany.type_user = UserType.objects.get(id=7)
            usercompany.email = AuthUser.objects.get(email=request.user.email)
            usercompany.user = AuthUser.objects.get(id=request.user.id)
            usercompany.save()
            return redirect('views.comapnylist',)

    else:
        form_company = CompanyForm()
    return render(request, 'companynew.html', {'form_company': form_company})


# CLIENTS
# clients list

def clients_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    clientslist = Client.objects.filter(company=mycompany).order_by('name')
    return render(request, 'clientslist.html', {'clientslist': clientslist})

# create new client


def clientsnew(request):

    if request.method == "POST":

        myclientform = ClientForm(request.POST)
        if myclientform.is_valid():
            newclient = myclientform.save(commit=False)
            newclient.company = Company.objects.get(
                owner_company=request.user.id)
            newclient.save()
            return redirect('planner_app.views.client_list', )

    else:
        myclientform = ClientForm()
    return render(request, 'clients.html', {'myclientform': myclientform})


# PORYECTOS


# Projects list

def projects_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    projectslist = Project.objects.filter(company=mycompany).order_by('client')
    return render(request, 'projectslist.html', {'projectslist': projectslist})

# create new project


def projectsnew(request):

    if request.method == "POST":
        projectsform = ProjectForm(request.user, request.POST)

        if projectsform.is_valid():
            newproject = projectsform.save(commit=False)
            newproject.company = Company.objects.get(
                owner_company=request.user.id)
            newproject.save()
            return redirect('views.projects_list', )

    else:
        projectsform = ProjectForm(request.user)
    return render(request, 'projects.html', {'projectsform': projectsform})


# DAY THAT THE COMPANY WORK

# day list

def weekday_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    weekdaylist = WeekDay.objects.filter(company=mycompany).order_by('daywork')
    return render(request, 'weekdaylist.html', {'weekdaylist': weekdaylist})

# new day


def weekdaynew(request):

    if request.method == "POST":
        # se apasan en el orden correcto request.user primero y prequest.POST
        # despes. El form primero se ejcuta el user y despues se pasa el POST
        weekdayform = WeekDayForm(request.user, request.POST)

        if weekdayform.is_valid():
            newday = weekdayform.save(commit=False)
            newday.company = Company.objects.get(owner_company=request.user.id)
            newday.save()
            return redirect('views.projects_list', )

    else:
        weekdayform = WeekDayForm(request.user)
    return render(request, 'weekday.html', {'weekdayform': weekdayform})


# COMPANY ScheduleCompany

# Company Schedule list

def schedulecompany_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    schedulecompanylist = ScheduleCompany.objects.filter(
        company=mycompany).order_by('company_week_day')
    return render(request, 'schedulecompanylist.html', {'schedulecompanylist': schedulecompanylist})

# new day


def schedulecompanynew(request):

    if request.method == "POST":
        schedulecompanyform = ScheduleCompanyForm(request.user, request.POST)
        if schedulecompanyform.is_valid():
            schedule = schedulecompanyform.save(commit=False)
            schedule.company = Company.objects.get(
                owner_company=request.user.id)
            schedule.save()
            return redirect('views.schedulecompany_list', )

    else:
        schedulecompanyform = ScheduleCompanyForm(request.user)
    return render(request, 'schedulecompany.html', {'schedulecompanyform': schedulecompanyform})


# REQUEST

# Request list

def request_list(request):
    myuser = request.user.id
    requestlist = Request.objects.filter(user=myuser).order_by(
        'week_number', 'resource', 'project')
    return render(request, 'requestlist.html', {'requestlist': requestlist})

# new request

+6
def requestnew(request):+6
+6
    if request.method == "POST":
        requestform = RequestForm(request.user, request.POST)

        if requestform.is_valid():
            requestnew = requestform.save(commit=False)
            requestnew.user = AuthUser.objects.get(id=request.user.id)
            requestnew.company = Company.objects.get(
                owner_company=request.user.id)
            requestnew.save()
            return redirect('views.request_list', )

    else:
        requestform = RequestForm(request.user)
    return render(request, 'request.html', {'requestform': requestform})


# USER HOLIDAYS -

 # holiday list

def userholidays_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    users = UserCompany.objects.filter(
        company=mycompany).values_list('pk', flat=True)
    holidaylist = UserHolidays.objects.filter(
        user__in=users).order_by('week')
    return render(request, 'holidaylist.html', {'holidaylist': holidaylist})

# new holiday


def userholidaysnew(request):

    if request.method == "POST":
        userholidaysform = UserHolidaysForm(request.user, request.POST)

        if userholidaysform.is_valid():
            userholidaysform.save()
            return redirect('views.schedulecompanyuser_list', )

    else:
        userholidaysform = UserHolidaysForm(request.user)
    return render(request, 'holiday.html', {'userholidaysform': userholidaysform})


# SCHEDULE USER  - ScheduleCompanyUser NO ESTÁ HECHA LA PAG. HAY QUE HACER
# LA PG DE LISTADO Y EDICION DE LAS HORAS

# schedule user list


def scheduleuser_list(request):
    mycompany = Company.objects.get(owner_company=request.user.id)
    users = UserCompany.objects.filter(
        company=mycompany).values_list('pk', flat=True)
    scheduleuserlist = ScheduleCompanyUser.objects.filter(
        user__in=users).order_by('schedule_company')
    return render(request, 'scheduleuserlist.html', {'scheduleuserlist': scheduleuserlist})

# new schedule user


def scheduleusernew(request):

    if request.method == "POST":
        scheduleuserform = UserHolidaysForm(request.user, request.POST)

        if scheduleuserform.is_valid():
            scheduleuserform.save()
            return redirect('views.scheduleuserform_list', )

    else:
        scheduleuserform = UserHolidaysForm(request.user)
    return render(request, 'scheduleuserform.html', {'scheduleuserform': scheduleuserform})


# CREACIÓN DE PLANIFICACIÓN

# Request list

def planning(request):

    mycompany = Company.objects.get(owner_company=request.user.id)

    # saber que semana es hoy
    today = datetime.date.today()
    weekpro = today.isocalendar()[1]

    # hacemos una lista de proyectos por semana para saber que
    # proyectos están repetidos de la semana pasada.
    # Los proyectos repetidos seran los primeros que planificaremos-

    repitpro = []
#=========================================================================

    for w in range(weekpro , weekpro + 2):
        nameprolist = Request.objects.filter(
            company=mycompany, week_number=w).values_list('project')
        repitpro += [(nameprolist)]

    # miro que proyecto se repite de esta semana y la pasada
    interpro = set(repitpro[0]).intersection(repitpro[1])

    # agrupo todas las planificaciones hechas de esos proyectos
    profirst = []
    for pr in interpro:
        reqtoplann = Request.objects.filter(project=pr).order_by(
            'week_number', 'resource').values_list('pk')
        profirst += [(reqtoplann)]

    # ahora la tupla lo convierto en una lista, y tengo el listado de todas
    # las planis que tengo que ir metiendo porque viene de la semana que viene
    profirst_list = [list(i) for i in profirst]
    print (profirst_list)

    # programo cada proyecto de la lista creada

    for prog in profirst_list[0]:
        print (prog[0])
        # identifico el proyecto
        prog_rec = Request.objects.get(pk=prog[0])
        print(prog_rec)

        # miro los dias que el proyecto tiene establcidos de trabajo
        listdays = range(prog_rec.day_week_in, prog_rec.day_week_out + 1)
        print (listdays)

        # miro las horas que trabaja el usuario en esos días y si tiene
        # vacaciones
# =========================================================================
        # hay que mirar como hacer todo esto en una clase
        # def hours_user_work(dayspro, userpro, comp, weekpro,)
# =========================================================================
        # saco las hora disponibles al dia del usuario diccionario (dia:hora)
        listhoursuser_t = []
        for listday in listdays:
            hoursuser = ScheduleCompanyUser.objects.get(
                user=prog_rec.resource, schedule_company=listday)
            listhoursuser_t += [(listday, hoursuser.hour)]
        print (listhoursuser_t)

        # saco las horas que tiene de vacaciones el usuaario en un dicionario
        # (dia:hora)
        listhoursholliday_t = []
        for listday in listdays:
            try:
                hoursuser_holliday = UserHolidays.objects.get(
                    user=prog_rec.resource, schedule_company=listday, week=weekpro + 1)
                listhoursholliday_t += [(listday, hoursuser_holliday.hour)]
            except UserHolidays.DoesNotExist:
                listhoursholliday_t += [(listday, 0)]
        print (listhoursholliday_t)

        # saco las horas que tiene en esa semana ya planificadas en un
        # dicionario (dia:hora)

        listnowplann_t = []
        for listday in listdays:
            try:
                houruser_plann = Planning.objects.get(
                    resource=prog_rec.resource, dayweek=listday, week=weekpro + 1)
                listnowplann_t += [(listday, houruser_plann)]
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
        print (real_hours_resource)

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
                        company=prog_rec.company,)]
                # si las horas restadas son menos que las
                # horas que hay en el dia pongo las horas que restan
                elif hoursneed != 0:
                    instances += [Planning(
                        project=prog_rec.project,
                        resource=prog_rec.resource,
                        week=prog_rec.week_number,
                        dayweek=plan[0],
                        hours=hoursneed,
                        company=prog_rec.company,)]

                else:
                    prog_rec.planned = True
                    prog_rec.save()
                    pass

            Planning.objects.bulk_create(instances)

        else:
            print('no lo planifico')
            pass



# =========================================================================
    # se ve en pantalla
    # lista todos las peticiones de recurso que hay

    myuser = request.user.id
    nameprolist = Request.objects.filter(user=myuser).order_by(
        'week_number', 'resource', 'project')

    return render(request, 'plannerlist.html', {'nameprolist': nameprolist})
