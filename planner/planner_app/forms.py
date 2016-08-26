from django import forms


# USER COMPANY

from .models import UserCompany, UserType, Company, Client, Project, WeekDay, ScheduleCompany, Request, AuthUser, DayName


class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = ()


class NewUserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = ('type_user', 'first_name', 'last_name', 'email')


# formulario instanciado
class UserTypeForm(forms.ModelForm):
    class Meta:
        model = UserType
        fields = ('type_user','role')

class MyUserCompanyForm(forms.ModelForm):

    class Meta:
        model = UserCompany
        fields = ('first_name', 'last_name', 'email','type_user',)

    def __init__(self, *args, **kwargs):
        super(MyUserCompanyForm, self).__init__(*args, **kwargs)
        self.queryset = forms.ModelChoiceField(queryset=UserType.objects.all())

# COMPANYS

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


# CLIENTS

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name',)


# PROYECTS

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('client', 'name',)
    def __init__(self, request, *args, **kwargs):
        # request is a required parameter for this form.
        super (ProjectForm,self ).__init__(*args,**kwargs)
        mycompany = Company.objects.get(owner_company=request.user.id)
        self.fields['client'].queryset = Client.objects.filter(company = mycompany)


# DAY THAT THE COMPANY WORK

class WeekDayForm(forms.ModelForm):
    class Meta:
        model = WeekDay
        fields = ('daywork',)

    #se reliza la funcion para coar el formauliro en su creación se pasa como parametro user, que viene de view. filtramos usuario, filtramos compañia, sacando solo los valores en una lista con value_list('valor', flat=true)
    def __init__(self, user, *args, **kwargs):
        self.user=user
        # request is a required parameter for this form.
        super (WeekDayForm,self ).__init__(*args,**kwargs)
        iduser = AuthUser.objects.filter(email = self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.filter(owner_company=iduser).values_list('name', flat=True)
        print (mycompany)
        mydays =  WeekDay.objects.filter(company = mycompany).values_list('daywork', flat=True)
        print (mydays)
        self.fields['daywork'].queryset = DayName.objects.exclude(dayname__in=mydays)


# DAY THAT THE COMPANY WORK - COMPANY SCHEDULE + HOURS

class ScheduleCompanyForm(forms.ModelForm):
    class Meta:
        model = ScheduleCompany
        fields = ('company_week_day', 'hours')

    def __init__(self, user, *args, **kwargs):
        self.user=user
        # request is a required parameter for this form.
        super (ScheduleCompanyForm,self ).__init__(*args,**kwargs)
        iduser = AuthUser.objects.filter(email = self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.filter(owner_company=iduser).values_list('name', flat=True)
        print (mycompany)
        mydayscomp =  ScheduleCompany.objects.filter(company = mycompany).values_list('company_week_day', flat=True)
        print (mydayscomp)
        self.fields['company_week_day'].queryset = WeekDay.objects.exclude(daywork__in=mydayscomp)



# REQUEST

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('project', 'time', 'resource','day_week_in','day_week_out','week_number',)

    def __init__(self, request, *args, **kwargs):
        # request is a required parameter for this form.
        super (RequestForm,self ).__init__(*args,**kwargs)
        mycompany = Company.objects.get(owner_company=request.user.id)
        self.fields['resource'].queryset = UserCompany.objects.filter(company = mycompany)






