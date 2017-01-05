
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

from collections import Counter


# LISTADO DE PROYCTOS PARA PLANIFICAR
class ListProjectsPlanning():

    def __init__(self, mycompany):
        self.mycompany = mycompany

    def listprojects(self):
        # lista de proyectos para planificar
        nameprolist = Petition.objects.filter(
            company=self.mycompany, planned=0,
            ).order_by('year').values_list('project')

        #cuento el numero de repeticiones de un proyecto
        repitpro = Counter(nameprolist)
        return repitpro

#LISTADO DE PLANIFICACIONES DE CADA PROYECTO
#ORDENADAS DE LOS QUE MAS HORA TIENEN A LOS QUE MENOS

class ListProjectsOkPlanning():

    def __init__(self, repitpro):
        self.repitpro = repitpro
    # agrupo todas las planificaciones hechas de esos proyectos
    # empezando por la que mas repeticiones tiene
    def listprojectsok(self):
        profirst = []
        for key, count in self.repitpro.most_common():
            reqtoplann = Petition.objects.filter(project=key).order_by(
                'year','week_number','resource').values_list('pk')
            profirst += [(reqtoplann)]

            return profirst


# HORAS DISPONIBLES DEL USUARIO
class UserHourWorkPlanning():

    def __init__(self, listdays, prog_rec, mycompany, *args, **kwargs):
        self.listdays = listdays
        self.prog_rec = prog_rec
        self.mycompany = mycompany

    def userhourwork(self):
        # miro las horas que trabaja el usuario en esos dias y si tiene
        # vacaciones
        # saco las hora disponibles al dia del usuario diccionario (dia:hora)
        listhoursuser_t = []
        for listday in self.listdays:
            hoursuser = ScheduleCompanyUser.objects.get(
                user=self.prog_rec.resource_id,
                schedule_company=ScheduleCompany.objects.get(
                    company=self.mycompany,
                    company_week_day=WeekDay.objects.get(
                        company=self.mycompany,
                        daywork=listday
                        )
                    )
                )
            listhoursuser_t += [(listday, hoursuser.hour)]
        print ('horario de usaurio', listhoursuser_t)

        return listhoursuser_t


# HORAS DE VACACIONES DEL USUARIO
class UserHourHollidayPlanning():

    def __init__(self, listdays, prog_rec, *args, **kwargs):
        self.listdays = listdays
        self.prog_rec = prog_rec

    def userhourholliday(self):
        # saco las horas que tiene de vacaciones el usuaario en un dicionario
        # (dia:hora)
        listhoursholliday_t = []
        for listday in self.listdays:
            try:
                hoursuser_holliday = UserHolidays.objects.get(
                    user=self.prog_rec.resource,
                    schedule_company=listday,
                    week=self.prog_rec.week_number
                    )
                listhoursholliday_t += [(listday, hoursuser_holliday.hour)]
            except UserHolidays.DoesNotExist:
                listhoursholliday_t += [(listday, 0)]
        print ('horas vacaciones', listhoursholliday_t)
        return listhoursholliday_t

# HORAS YA PLANIFICADAS DEL USUARIO
class UserHourPlannedPlanning():

    def __init__(self, listdays, prog_rec, year,*args, **kwargs):
        self.listdays = listdays
        self.prog_rec = prog_rec
        self.year = year

    def userhourplanned(self):
        # saco las horas que tiene en esa semana ya planificadas en un
        # dicionario (dia:hora)
        listnowplann_t = []
        for listday in self.listdays:
            try:
                print ('llego hasta aqui')
                houruser_plann = Planning.objects.get(
                    resource=self.prog_rec.resource_id,
                    dayweek=listday,
                    week=self.prog_rec.week_number,
                    year=self.year)
                print ('mirar', houruser_plann)
                listnowplann_t += [(listday, houruser_plann.hours)]
            except Planning.DoesNotExist:
                listnowplann_t += [(listday, 0)]
        print ('horas disponibles: '), (listnowplann_t)
        return listnowplann_t

# MIRA LAS HORAS DEL PROYECTO Y LAS HORAS DISPONIBLES DEL RECURSO
# SI TIENE HORA DISPONBILES ENTONCES LO PLANIFICA
class HorsProjectsUserPlanning():

    def __init__(self, profirst,year, mycompany, *args, **kwargs):
        self.profirst = profirst
        self.year = year
        self.mycompany = mycompany

    def horasprojectsuser(self):
        for listproj in self.profirst:
            print ('listproj:',listproj)
            # todos las planificaciones por proyecto
            profirst_list = []
            # todas la horas por proyecto
            projectalltime = []
            # todas las horas de usuario por lo que dura el proyecto
            useralltime = []
            dic_weekandhours = []
            for prog in listproj:

                print('prog', prog)

                profirst_list.append(prog)

                # programo cada proyecto de la lista creada
                # identifico el proyecto
                prog_rec = Petition.objects.get(pk=prog[0])

                # miro los dias que el proyecto tiene establcidos de trabajo
                listdays = range(prog_rec.day_week_in, prog_rec.day_week_out + 1)
                print('listdays',listdays)
                # miro las horas que trabaja el usuario en esos dias y si tiene
                # vacaciones
                # saco las hora disponibles al dia del usuario diccionario (dia:hora)
                listhoursuser_t = UserHourWorkPlanning(listdays,prog_rec,self.mycompany).userhourwork()


                # saco las horas que tiene de vacaciones el usuaario en un dicionario
                # (dia:hora)
                listhoursholliday_t = UserHourHollidayPlanning(listdays,prog_rec).userhourholliday()

                # saco las horas que tiene en esa semana ya planificadas en un
                # dicionario (dia:hora)
                listnowplann_t = UserHourPlannedPlanning(listdays,prog_rec,self.year).userhourplanned()

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

                projectalltime.append(prog_rec.time)
                useralltime.append(total_listhours)

                real_hours_resource_ord = sorted(real_hours_resource)
                print ('real_hours_resource_ord:', real_hours_resource_ord)

                dic_weekandhours.append([(prog[0], real_hours_resource_ord)])

            # sumo el total de horas del proyecto y del usuario
            total_project_time = sum(projectalltime)
            print('total_project_time:', total_project_time)
            total_user_time = sum(useralltime)
            print ('total_user_time:', total_user_time)

            print('dic_weekandhours:', dic_weekandhours)

            if total_user_time < total_project_time:
                print ('no se planifica:', profirst_list)

            else:
                print ('si se planifica:', profirst_list)
                #return profirst_list,total_project_time,total_user_time
                print('totales:',profirst_list,total_user_time,total_project_time)
                PlannedOkPlanning(dic_weekandhours).plannedok()



class PlannedOkPlanning():
    def __init__(self, dic_weekandhours):
        self.dic_weekandhours = dic_weekandhours

    def plannedok(self):
        for weekplann in self.dic_weekandhours:
            weekplann_ok=weekplann[0]
            instances = []

            project_plan = Petition.objects.get(id=weekplann_ok[0])
            print('project_plan', project_plan)
            print('test')
            hoursneed =  project_plan.time
            print('hoursneed', hoursneed)
            hoursdisp =weekplann_ok[1]
            print('hoursdisp',hoursdisp)

            # voy restando las horas a las horas del proyecto
            for plan in hoursdisp:
                print(hoursneed)
                if plan[1] <= hoursneed:
                    hoursneed -= plan[1]
                    instances += [Planning(
                        project=project_plan.project,
                        resource=project_plan.resource,
                        week=project_plan.week_number,
                        dayweek=plan[0],
                        hours=plan[1],
                        company=project_plan.company,
                        year=project_plan.year)]

                # si las horas restadas son menos que las
                # horas que hay en el dia pongo las horas que restan
                elif hoursneed != 0:
                    instances += [Planning(
                        project=project_plan.project,
                        resource=project_plan.resource,
                        week=project_plan.week_number,
                        dayweek=plan[0],
                        hours=hoursneed,
                        company=project_plan.company,
                        year=project_plan.year)]
                    hoursneed -= hoursneed
                else:
                    pass

            project_plan.planned = True
            project_plan.save()
            Planning.objects.bulk_create(instances)
            print('planifico')
