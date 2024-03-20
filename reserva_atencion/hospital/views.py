from django.shortcuts import render
from .models import Medico, Atencion

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

    info_semana = get_semana(2024, 3, 20)

    print(info_semana)

    
    #for i in 


    fecha_inicio = info_semana["semana"][0][1]
    fecha_termino = info_semana["semana"][-1][1]
    
    atenciones = Atencion.objects.filter(fecha_atencion__gte=fecha_inicio, fecha_atencion__lte=fecha_termino)
    print(atenciones)

    c = {
        "atenciones": atenciones,
        "horarios": [
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
    }

    return render(request, "reservar_atencion.html", context=c)






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
    semana = []
    for d in zip(nombres_dias, fechas_semana):
        semana.append(d)

    info_semana["hoy"] = date(year, month, day)
    info_semana["semana"] = semana

    return info_semana





def medicos(request):
    # se recuperan todos los medicos
    medicos = Medico.objects.all()
    lista_medicos = {"medicos": medicos}

    return render(request, "medicos.html", lista_medicos)