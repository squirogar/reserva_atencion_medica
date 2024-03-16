from django.shortcuts import render
from .models import Medico

# Create your views here.

def historial(request):
    # se recuperan todas las atenciones del usuario
    historial = {}

    return render(request, "historial.html", context=historial)



def reservar_hora(request):
    # reserva hora
    c = {}

    return render(request, "reservar_hora.html", context=c)


def medicos(request):
    # se recuperan todos los medicos
    medicos = Medico.objects.all()
    lista_medicos = {"medicos": medicos}

    return render(request, "medicos.html", lista_medicos)