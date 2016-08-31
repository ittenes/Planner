from django.shortcuts import render
from django.shortcuts import redirect
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


def requestnew(request):

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


# SCHEDULE USER  - ScheduleCompanyUser NO ESTÁ HECHA LA PAG. HAY QUE HACER LA PG DE LISTADO Y EDICION DE LAS HORAS

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


    requestlist = Request.objects.filter(company=mycompany).order_by(
        'week_number', 'resource', 'project')
    return render(request, 'requestlist.html', {'requestlist': requestlist})






















