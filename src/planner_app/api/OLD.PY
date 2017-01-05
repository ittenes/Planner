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


        def listprojects():

            # lista de proyectos para planificar
            nameprolist = Petition.objects.filter(
                company=mycompany, planned=0,
                ).order_by('year').values_list('project')

            #cuento el numero de repeticiones de un proyecto
            repitpro = Counter(nameprolist)
            return repitpro

        # cojo los proyectos para planificar
        repitpro = listprojects()
        print ('repitpro:', repitpro)

        def listprojectsok(repitpro):
            # agrupo todas las planificaciones hechas de esos proyectos
            # empezando por la que mas repeticiones tiene
            profirst = []
            for key, count in repitpro.most_common():
                reqtoplann = Petition.objects.filter(project=key).order_by(
                    'year','week_number','resource').values_list('pk', flat=True)
                reqtoplanns = list(reqtoplann)
                profirst += [(reqtoplanns)]

            return profirst


        # listo los proyectos con sus planificaciones
        profirsts = listprojectsok(repitpro)

        print ('profirsts:', profirsts)

        def horsprojectsuser(profirst, **kwargs):

            for listproj in profirst:
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
                    prog_rec = Petition.objects.get(pk=prog)

                    # miro los dias que el proyecto tiene establcidos de trabajo
                    listdays = range(prog_rec.day_week_in, prog_rec.day_week_out + 1)

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

                    projectalltime.append(prog_rec.time)
                    useralltime.append(total_listhours)

                    real_hours_resource_ord = sorted(real_hours_resource)
                    print ('real_hours_resource_ord:', real_hours_resource_ord)

                    dic_weekandhours.append([prog, real_hours_resource_ord])

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

                    def planned(dic_weekandhours):
                        print('lo planifico')
                        for weekplann in dic_weekandhours:

                            instances = []
                            project_plan = Petition.objects.get(id=weekplann[0])
                            hoursneed =  project_plan.time
                            print('hoursneed', hoursneed)
                            hoursdisp =weekplann[1]
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
                            print('planifico', prog_rec.week_number )

                    planned(dic_weekandhours)


        plannnedok = horsprojectsuser(profirsts)
        print('plannnedok:',plannnedok)
