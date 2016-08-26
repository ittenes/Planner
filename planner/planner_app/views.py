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

from .forms import UserCompanyForm
from .forms import NewUserCompanyForm
from .forms import MyUserCompanyForm
from .forms import CompanyForm
from .forms import ClientForm
from .forms import ProjectForm
from .forms import WeekDayForm
from .forms import ScheduleCompanyForm
from .forms import RequestForm


# USER COMPANY
# users list

def user_company_list(request):
    myuser = Company.objects.get(owner_company=request.user.id)
    usercompanys = UserCompany.objects.filter(company=myuser).order_by()
    return render(request, 'usercompanylist.html',
                  {'usercompanys': usercompanys})


def myusercompany(request):
    if request.method == "POST":

        myusercompanyform = MyUserCompanyForm(request.POST, )
        if myusercompanyform.is_valid():
            myuserform = myusercompanyform.save(commit=False)
            myuserform.company = Company.objects.get(
                owner_company=request.user.id)
            myuserform.user = AuthUser.objects.get(id=request.user.id)
            myuserform.save()
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
            print('inicio')
            company = form_company.save(commit=False)
            company.owner_company = AuthUser.objects.get(id=request.user.id)
            company.active = "1"
            company.save()
            print('medio')
            # when creta the new company save de user in de user_company how
            #    owner of the company
            usercompany = form_usercompanyactive.save(commit=False)
            usercompany.company = Company.objects.get(
                owner_company=request.user.id)
            usercompany.type_user = UserType.objects.get(id=7)
            usercompany.email = AuthUser.objects.get(email=request.user.email)
            usercompany.user = AuthUser.objects.get(id=request.user.id)
            usercompany.save()
            print('fnial')
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
    myproject = Company.objects.get(owner_company=request.user.id)
    projectslist = Project.objects.filter(company=myproject).order_by('client')
    return render(request, 'projectslist.html', {'projectslist': projectslist})

# create new project


def projectsnew(request):

    if request.method == "POST":
        projectsform = ProjectForm(request.POST,request.FILES)

        if projectsform.is_valid():
            newproject = projectsform.save(commit=False)
            newproject.company = Company.objects.get(owner_company=request.user.id)
            newproject.save()
            return redirect('views.projects_list', )

    else:
        projectsform = ProjectForm(request=request)
    return render(request, 'projects.html', {'projectsform': projectsform})


# DAY THAT THE COMPANY WORK

# day list

def weekday_list(request):
    weekdaylist = WeekDay.objects.filter().order_by()
    return render(request, 'weekdaylist.html', {'weekdaylist': weekdaylist})

# new day


def weekdaynew(request):

    if request.method == "POST":
        #se apasan en el orden correcto request.user primero y prequest.POST despes. El form primero se ejcuta el user y despues se pasa el POST
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
    myschedule = Company.objects.get(owner_company=request.user.id)
    schedulecompanylist = ScheduleCompany.objects.filter(company=myschedule).order_by('company_week_day')
    return render(request, 'schedulecompanylist.html', {'schedulecompanylist': schedulecompanylist})

# new day


def schedulecompanynew(request):

    if request.method == "POST":
        schedulecompanyform = ScheduleCompanyForm(request.user, request.POST)
        if schedulecompanyform.is_valid():
            schedule = schedulecompanyform.save(commit=False)
            schedule.company = Company.objects.get(owner_company=request.user.id)
            schedule.save()
            return redirect('views.schedulecompany_list', )

    else:
        schedulecompanyform = ScheduleCompanyForm(request.user)
    return render(request, 'schedulecompany.html', {'schedulecompanyform': schedulecompanyform})


# REQUEST

# Request list

def request_list(request):
    myrequest = request.user.id
    requestlist = Request.objects.filter(user=myrequest).order_by('project')
    return render(request, 'requestlist.html', {'requestlist': requestlist})

# new day


def requestnew(request):

    if request.method == "POST":
        requestform = RequestForm(request.POST, request.FILES)

        if requestform.is_valid():
            requestnew = requestform.save(commit=False)
            requestnew.user = AuthUser.objects.get(id=request.user.id)
            requestnew.company = Company.objects.get(owner_company=request.user.id)
            requestnew.save()
            return redirect('views.request_list', )

    else:
        requestform = RequestForm(request=request)
    return render(request, 'request.html', {'requestform': requestform})








