from django import forms
import datetime

# USER COMPANY

from .models import UserCompany, UserType, Company, Client, Project, WeekDay, ScheduleCompany, Request, AuthUser, DayName, UserHolidays, ScheduleCompanyUser


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
        fields = ('type_user', 'role')


class MyUserCompanyForm(forms.ModelForm):

    class Meta:
        model = UserCompany
        fields = ('first_name', 'last_name', 'email', 'type_user',)

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

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # request is a required parameter for this form.
        super(ProjectForm, self).__init__(*args, **kwargs)
        iduser = AuthUser.objects.filter(email=self.user).values('id')
        print (iduser)
        mycompany = Company.objects.filter(
            owner_company=iduser).values_list('id', flat=True)
        print (mycompany)
        self.fields['client'].queryset = Client.objects.filter(
            company=mycompany)


# DAY THAT THE COMPANY WORK

class WeekDayForm(forms.ModelForm):
    class Meta:
        model = WeekDay
        fields = ('daywork',)

    # se reliza la funcion para coar el formauliro en su creacion se pasa como
    # parametro user, que viene de view.
    # Filtramos usuario, filtramos compania, sacando solo los valores en una
    # lista con value_list('valor',flat=true)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # request is a required parameter for this form.
        super(WeekDayForm, self).__init__(*args, **kwargs)
        iduser = AuthUser.objects.filter(email=self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.filter(
            owner_company=iduser).values_list('id', flat=True)
        print (mycompany)
        mydays = WeekDay.objects.filter(
            company=mycompany).values_list('daywork', flat=True)
        print (mydays)
        self.fields['daywork'].queryset = DayName.objects.exclude(
            dayname__in=mydays)


# DAY THAT THE COMPANY WORK - COMPANY SCHEDULE + HOURS

class ScheduleCompanyForm(forms.ModelForm):
    class Meta:
        model = ScheduleCompany
        fields = ('company_week_day', 'hours')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # request is a required parameter for this form.
        super(ScheduleCompanyForm, self).__init__(*args, **kwargs)
        iduser = AuthUser.objects.filter(email=self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.get(owner_company=iduser)
        print (mycompany)
        mydayscomp = ScheduleCompany.objects.filter(
            company=mycompany).values_list('company_week_day', flat=True)
        print (mydayscomp)
        self.fields['company_week_day'].queryset = WeekDay.objects.filter(
            company=mycompany).exclude(id__in=mydayscomp)


# REQUEST

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('project', 'time', 'resource', 'day_week_in',
                  'day_week_out', 'week_number',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # request is a required parameter for this form.
        super(RequestForm, self).__init__(*args, **kwargs)
        # only show the resources of de user company
        iduser = AuthUser.objects.filter(email=self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.filter(
            owner_company=iduser).values_list('id', flat=True)
        print (mycompany)
        self.fields['project'].queryset = Project.objects.filter(
            company=mycompany)
        self.fields['resource'].queryset = UserCompany.objects.filter(
            company=mycompany)
        # select de week's number. only allow select this week or one of the
        # the next five

        today = datetime.date.today()
        print (today)
        week = today.isocalendar()[1]
        print (week)
        weekfive = [(week + 1, week + 1),
                    (week + 2, week + 2),
                    (week + 3, week + 3),
                    (week + 4, week + 4),
                    (week + 5, week + 5)]
        print (weekfive)
        self.fields['week_number'] = forms.ChoiceField(
            widget=forms.Select(), choices=weekfive, required=True)


# USER HOLLYDAYS -

class UserHolidaysForm(forms.ModelForm):
    class Meta:
        model = UserHolidays
        fields = ('user', 'schedule_company', 'hour', 'week')

    def __init__(self, user, *args, **kwargs):
        self.user = user

        super(UserHolidaysForm, self).__init__(*args, **kwargs)
        iduser = AuthUser.objects.filter(email=self.user).values('pk')
        print (iduser)
        mycompany = Company.objects.filter(
            owner_company=iduser).values_list('id', flat=True)
        print (mycompany)
        daysmycompany = ScheduleCompany.objects.filter(
            company__in=mycompany).values_list('company_week_day', flat=True)
        print (daysmycompany)
        self.fields['schedule_company'].queryset = ScheduleCompany.objects.filter(
            company__in=mycompany)

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
            if weeklast > 0:
                twotuple += [(keyallweek, valueallweek)]
        print (twotuple)
        self.fields['week'] = forms.ChoiceField(
            widget=forms.Select(), choices=twotuple, required=True)


# USER SCHEDULE - ScheduleCompanyUser

class ScheduleCompanyUserForm(forms.ModelForm):
    class Meta:
        model = ScheduleCompanyUser
        fields = ()









