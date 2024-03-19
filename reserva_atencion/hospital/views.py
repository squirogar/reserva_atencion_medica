from django.shortcuts import render
from .models import Medico, Atencion

from datetime import datetime

# Create your views here.

def historial(request):
    # se recuperan todas las atenciones del usuario
    historial = {}

    return render(request, "historial.html", context=historial)



def reservar_atencion(request):
    # reserva atencion

    atenciones = Atencion.objects.all()
    print(atenciones)

    c = {
        "atenciones": atenciones,
        "horarios": [
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
    }

    return render(request, "reservar_atencion.html", context=c)


def get_semana():
    # saber el dia actual
    hoy = datetime.datetime.now()

    # saber cuantos dias quedan de la semana 
    # [dia_actual+1, Viernes]
    numero_dia = calendar.weekday(hoy.year,hoy.month,hoy.day) # numero_dia: [0-6]
    dias_restantes_semana = 4 - numero_dia

    
    # retornar 
    # - nombres dias de la semana restante
    # - fechas de estos dias (sin la hora)
    for i in range(dias_restantes_semana):
        calendar.weekday(hoy.year,hoy.month,hoy.day)



def medicos(request):
    # se recuperan todos los medicos
    medicos = Medico.objects.all()
    lista_medicos = {"medicos": medicos}

    return render(request, "medicos.html", lista_medicos)