from django.contrib import admin


# formularios desde al admin
from .models import Client
from .models import Company
from .models import Planning
from .models import Project
from .models import Provider
from .models import Role
from .models import ScheduleCompany
from .models import ScheduleCompanyUser
from .models import UserCompany
from .models import UserHolidays
from .models import UserType
from .models import WeekDay
from .models import DayName

# Register your models here.
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Planning)
admin.site.register(Project)
admin.site.register(Provider)
admin.site.register(Role)
admin.site.register(ScheduleCompany)
admin.site.register(ScheduleCompanyUser)
admin.site.register(UserCompany)
admin.site.register(UserHolidays)
admin.site.register(UserType)
admin.site.register(WeekDay)
admin.site.register(DayName)
