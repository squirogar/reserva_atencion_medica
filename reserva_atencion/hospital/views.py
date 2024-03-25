from django.shortcuts import render, HttpResponse
from .models import Medico, Atencion


from . import utils

from datetime import date
import calendar
import locale

# Create your views here.

# cambiamos el locale para que los dias de semana sean en español
locale.setlocale(locale.LC_ALL, 'es_Es')


def historial(request):
    # se recuperan todas las atenciones del usuario
    historial = {}

    return render(request, "historial.html", context=historial)



def reservar_atencion(request):
    # reserva atencion

    fechas_semana = get_semana(2024, 3, 20)

    print(fechas_semana)

    """
    horarios= [
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
    
    print("\naca estamos comprobando las atenciones para un dia\n")

    semana = []    

    for i in range(len(fechas_semana["semana"])):
        print("\t\tDIA:", fechas_semana["semana"][i][0])
        print(type(fechas_semana["semana"][i][1]))
        # atenciones para un dia especifico de la semana
        atenciones_dia = Atencion.objects.filter(fecha_atencion=fechas_semana["semana"][i][1])
        print(atenciones_dia, "\n")

        # vamos pregunta por cada horario los medicos disponibles
        lista_horas = []
        for hora in horarios:
            print("\t hora", hora)
            # Utilizamos exclude() en el modelo Medico para excluir aquellos médicos 
            # que tienen una atención programada a una determinada hora.
            #medicos_disponibles = Medico.objects.exclude(atencion__hora_atencion=hora, atencion__fecha_atencion=fechas_semana["semana"][i][1])
            atencion_con_hora_fecha = Atencion.objects.filter(hora_atencion=hora, fecha_atencion=fechas_semana["semana"][i][1])
            medicos_con_atencion = atencion_con_hora_fecha.values_list('medico_id', flat=True)
            medicos_disponibles = Medico.objects.exclude(id__in=medicos_con_atencion)
            print("medicos disponibles: ", medicos_disponibles)
            #atenciones_hora = atenciones_dia.filter(hora_atencion=hora)
            #print("atenciones_hora", atenciones_hora)

            if medicos_disponibles:
                # guardamos la lista de medicos en algun lugar junto con la hora
                lista_horas.append(utils.Hora(hora, medicos_disponibles))

        
        # guardamos los dias con su fecha y con sus horas disponibles
        semana.append(utils.DiaAtencion(
            dia=fechas_semana["semana"][i][0], 
            fecha=fechas_semana["semana"][i][1],
            lista_horas=lista_horas)
        )

    """
    contexto = {
        "hoy": fechas_semana["hoy"],
        "semana": fechas_semana["semana"],
    }





    

    return render(request, "reservar_atencion.html", context=contexto)



################
from django.http import JsonResponse

def get_horas_disponibles(request):
    print("\n\n\nHORAS DISPONIBLES AJAX")
    fecha = request.GET.get('fecha')
    print(fecha)
    atenciones_del_dia = Atencion.objects.filter(fecha_atencion=fecha)
    print(atenciones_del_dia, "\n")


    ###
    # vamos pregunta por cada horario los medicos disponibles
    opciones = []
    horarios= [
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
    
    
    for hora in horarios:
        print("\t hora", hora)
        # Utilizamos exclude() en el modelo Medico para excluir aquellos médicos 
        # que tienen una atención programada a una determinada hora.
        #medicos_disponibles = Medico.objects.exclude(atencion__hora_atencion=hora, atencion__fecha_atencion=fechas_semana["semana"][i][1])
        atencion_con_hora_fecha = Atencion.objects.filter(hora_atencion=hora, fecha_atencion=fecha)
        medicos_con_atencion = atencion_con_hora_fecha.values_list('medico_id', flat=True)
        medicos_disponibles = Medico.objects.exclude(id__in=medicos_con_atencion)
        print("medicos disponibles: ", medicos_disponibles)
        print(list(medicos_disponibles.values_list("id", "nombre", "apellido")))
        #atenciones_hora = atenciones_dia.filter(hora_atencion=hora)
        #print("atenciones_hora", atenciones_hora)

        if medicos_disponibles:
            # guardamos la lista de medicos en algun lugar junto con la hora
            opciones.append({"hora": hora, "medicos": list(medicos_disponibles.values_list("id", "nombre", "apellido"))})
            # opciones = [{hora: lista de medicos disponibles}, ..., {hora: lista de medicos disponibles}]

    return JsonResponse({'opciones': opciones})


    ###




def get_medicos_disponibles(request):
    print("jfdj")
    selected_value = request.GET.get('selected_value')

    # Aquí realiza la lógica para consultar la base de datos y obtener las opciones para el segundo dropdown
    # Supongamos que tienes una lista de opciones en forma de tuplas (value, label)
    options = [
        {'value': 1, 'label': 'Opción A'},
        {'value': 2, 'label': 'Opción B'},
        {'value': 3, 'label': 'Opción C'}
    ]

    return JsonResponse({'options': options})

################

def reserva_atencion_medica(request):
    print("aloha")
    return HttpResponse("aloha")







def get_semana(year, month, day):

    c = calendar.Calendar()

    
    #hoy = datetime.datetime.now() # saber la fecha actual
    numero_dia_hoy = calendar.weekday(year, month, day) # numero_dia actual: [0-6]
    dia = calendar.day_name[numero_dia_hoy] # dia de la semana que es hoy

    print(numero_dia_hoy, dia)

    # queremos saber en que semana esta el dia de hoy
    mes = c.monthdayscalendar(year, month)

    fechas_semana = None
    nombres_dias = None

    # si el dia actual es domingo y es ultimo dia del mes. 
    if mes[-1][-1] == day: 
        
        # obtenemos los nombres de los dias de la semana 
        nombres_dias = [calendar.day_name[d] for d in range(0, 7)]
        
        if month == 12: # si es diciembre
            # obtenemos la primera semana de enero del año siguiente
            fechas_semana = c.monthdatescalendar(year+1, 1)[0]
        
        else:
            # obtenemos la primera semana del mes siguiente
            fechas_semana = c.monthdatescalendar(year, month+1)[0]
            
    else:
        num_semana = 0 # semana correspondiente a hoy. num_semana=0=primera semana del mes
        for semana in mes:
            if day in semana:
                print(f"hoy.day {day}, semana {semana}, hoy.month {month}")
                break
            num_semana += 1        

        
        if numero_dia_hoy == 6: # si hoy es domingo
            num_semana += 1 # queremos la semana siguiente
            numero_dia_hoy = 0 # consideramos hoy = lunes


        # obtenemos las fechas de toda la semana actual
        fechas_semana = c.monthdatescalendar(year, month)[num_semana]

        # guardamos solo las fechas de los dias restantes de la semana [hoy,..., domingo]
        fechas_semana = fechas_semana[numero_dia_hoy:]

        # obtenemos los nombres de los dias restantes de la semana [hoy,..., domingo]
        nombres_dias = [calendar.day_name[d] for d in range(numero_dia_hoy, 7)]



    # guardamos cada dia con su correspondiente fecha (nombre_dia, fecha)
    info_semana = {}
    semana = {}
    for d, f in zip(nombres_dias, fechas_semana):
        semana[d] = f

    print(semana)
    info_semana["hoy"] = date(year, month, day)
    info_semana["semana"] = semana

    return info_semana





def medicos(request):
    # se recuperan todos los medicos
    medicos = Medico.objects.all()
    lista_medicos = {"medicos": medicos}

    return render(request, "medicos.html", lista_medicos)