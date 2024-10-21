from django.shortcuts import render, redirect
from .models import Medico, Atencion, Box
from feriados.models import Feriados
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

import calendar
import locale
from .utils_hosp import get_fecha_hora_hoy, formatea_fecha, crea_fecha, crea_hora
from . import horarios_hosp

from django.db import IntegrityError


# Create your views here.

# cambiamos el locale para que los dias de semana sean en español
locale.setlocale(locale.LC_ALL, 'es_Es')




### vistas simples de recuperacion de datos ###
@login_required(login_url="auth:login")
def historial(request):
    # se recuperan el usuario conectado
    usuario = Usuario.objects.get(username=request.user.username)
    
    # se recuperan todas las atenciones del usuario
    atenciones_usuario = Atencion.objects.filter(usuario=usuario.id).select_related("medico__box").order_by("id")

    contexto = {
        "usuario": usuario.username,
        "atenciones": atenciones_usuario
    }
    
    return render(request, "hospital/historial.html", context=contexto)



@login_required(login_url="auth:login")
def medicos(request):
    # se recuperan todos los medicos y los boxes donde trabajan
    medicos_con_box = Medico.objects.select_related("box")

    lista_medicos = {"medicos": medicos_con_box}

    return render(request, "hospital/medicos.html", lista_medicos)





### vistas que procesan la reserva de atención ###

@login_required(login_url="auth:login")
def reservar_atencion(request):
    
    contexto = {}
    
    info = habilitado_para_reservar(request.user.username)
    
    contexto["codigo"] = info["codigo"]

    
    if info["codigo"] == 0: # si el usuario esta habilitado

        # obtenemos los días restantes de la semana
        dia_de_hoy = get_fecha_hora_hoy()
        fechas_semana = get_semana(dia_de_hoy.year, dia_de_hoy.month, dia_de_hoy.day)

        # limpiamos la semana
        semana_limpia = limpia_semana(fechas_semana["semana"], dia_de_hoy)

        if semana_limpia != {}:
            # guardamos los datos de la semana en el contexto
            contexto["hoy"] = fechas_semana["hoy"]
            contexto["semana"] = semana_limpia

        else:
            contexto["codigo"] = 1
    
    elif info["codigo"] == 2:
        # si el usuario no esta habilitado porque ya tiene una reserva activa
        # guardamos la fecha y hora de la ultima atencion reservada en el contexto
        contexto["fecha_ultima_atencion"] = info["ultima_atencion"].fecha_atencion.strftime("%d-%m-%Y")
        contexto["hora_ultima_atencion"] = info["ultima_atencion"].hora_atencion.strftime("%H:%M")

    
    return render(request, "hospital/reservar_atencion.html", context=contexto)



def habilitado_para_reservar(usuario):
    """
    Retorna un código que es un entero que indica si el usuario conectado puede reservar 
    una atencion. Este entero puede tener uno de estos 3 valores:
    - 0: el usuario puede reservar una atención
    - 1: el usuario no puede reservar una atención, ya que es sábado, o domingo 
    antes de las 17:00 hrs.
    - 2: el usuario no puede reservar una atención, ya que tiene una reserva
    de atención que aún no expira (fecha y hora de hoy <= fecha y hora de atencion). 
    
    Args: 
    - usuario (str): nombre de usuario conectado

    Returns:
    - dict: con un codigo (int) y un objeto de tipo hospital.models.Atencion en el caso
    que el código sea 2.

    """

    codigo = -1
    ultima_atencion_reservada = None


    hoy = get_fecha_hora_hoy()
    hora_hoy = hoy.time() # tiempo actual
    dia_semana = calendar.weekday(hoy.year, hoy.month, hoy.day) # [0-6]
    
    # si es sabado, o (domingo y la hora < 17:00)
    if dia_semana == 5 or (dia_semana == 6 and hora_hoy < crea_hora(17,0,0)): 
        codigo = 1

    else:

        # comprobamos si el usuario ya tiene una reserva activa, o sea,
        # aun no expira la reserva de atencion.
        id_usuario_conectado = Usuario.objects.get(username=usuario).id

        atenciones_usuario_conectado = Atencion.objects.filter(usuario_id=id_usuario_conectado)

        if atenciones_usuario_conectado: # si tiene atenciones
            ultima_atencion_reservada = atenciones_usuario_conectado.latest("fecha_reserva")
                                    
            fecha_atencion_ultima_reserva = ultima_atencion_reservada.fecha_atencion
            hora_atencion_ultima_reserva = ultima_atencion_reservada.hora_atencion
            

            # preguntamos si aun no ha expirado la reserva
            hora_hoy = hoy.time().replace(microsecond=0)

            if hoy.date() < fecha_atencion_ultima_reserva: 
                codigo = 2

            elif hoy.date() == fecha_atencion_ultima_reserva and hora_hoy <= hora_atencion_ultima_reserva:
                codigo = 2

            else:
                codigo = 0
            

        else: # si no tiene atenciones
            codigo = 0


    return {"codigo": codigo, "ultima_atencion": ultima_atencion_reservada}




def get_semana(year, month, day):
    """
    Devuelve los días restantes de la semana de acuerdo a una fecha consultada.

    Args:
    - year (int): año
    - month (int): mes
    - day (int): día

    Returns:
    - dict con la fecha consultada y las fechas de los días restantes de la semana.
    """


    ## obtención número y nombre del día de la fecha consultada ##
    c = calendar.Calendar()        
    numero_dia = calendar.weekday(year, month, day) # [0-6]
    nombre_dia = calendar.day_name[numero_dia] # [lun,..., dom]


    ## obtención de la semana en la que está la fecha consultada ##

    # monthdayscalendar() retorna una lista de las semanas del mes
    # como semanas completas.
    mes = c.monthdayscalendar(year, month)

    fechas_semana = None # lista de objetos tipo datetime.date
    nombres_dias = None # lista de strings

    # si el dia consultado es domingo y es ultimo dia del mes. 
    if mes[-1][-1] == day: 
        
        # obtenemos los nombres de los dias de la semana 
        nombres_dias = [calendar.day_name[d] for d in range(0, 7)]
        
        # monthdatescalendar() en vez de retornar una lista con
        # números como monthdayscalendar() de la semanas del mes,
        # retorna objetos de tipo datetime.date.

        if month == 12: # si es diciembre
            # obtenemos la primera semana de enero del año siguiente
            fechas_semana = c.monthdatescalendar(year+1, 1)[0]
        
        else:
            # obtenemos la primera semana del mes siguiente
            fechas_semana = c.monthdatescalendar(year, month+1)[0]
            
    else:
        # obtenemos la semana a la que pertenece la fecha consultada
        numero_semana = 0 # num_semana=0: primera semana del mes
        for semana in mes:
            if day in semana:
                print(f"hoy.day {day}, semana {semana}, hoy.month {month}")
                break
            numero_semana += 1        

        # en caso de que el día sea domingo, obtenemos la semana siguiente
        if numero_dia == 6: 
            numero_semana += 1 
            numero_dia = 0 # lunes


        # obtenemos las fechas de toda la semana
        fechas_semana = c.monthdatescalendar(year, month)[numero_semana]

        # guardamos solo las fechas de los dias restantes de la semana [numero_dia,...,dom]
        fechas_semana = fechas_semana[numero_dia:]

        # obtenemos los nombres de los dias restantes de la semana [numero_dia,...,domingo]
        nombres_dias = [calendar.day_name[d] for d in range(numero_dia, 7)]



    ## guardamos cada dia con su correspondiente fecha ##
    info_semana = {}
    semana = {}
    for d, f in zip(nombres_dias, fechas_semana):
        semana[d] = f


    info_semana["hoy"] = crea_fecha(year, month, day)
    info_semana["semana"] = semana

    return info_semana




def limpia_semana(semana, hoy):
    """
    Elimina de la semana los feriados, los sábados y domingos, y el 
    día de hoy en el caso que la hora actual sea mayor a 7:30 hrs. 
    Retorna un diccionario con las fechas de los días que quedan.
    Args:
    - semana (dict): {dia: fecha}
    - hoy (datetime.datetime)
    Returns:
    - semana (dict): {dia: fecha}
    """

    # eliminamos sabado y domingo
    del semana["sábado"]
    del semana["domingo"]


    # eliminamos los feriados
    semana_copia = dict(semana)
    for d, f in semana_copia.items():
        if Feriados.objects.filter(fecha=f).exists():
            del semana[d]
    

    # si consideramos o no el dia de hoy para pedir hora
    hora_hoy = hoy.time()   
    dia = calendar.day_name[calendar.weekday(hoy.year, hoy.month, hoy.day)] # dia de la semana que es hoy


    if semana.get(dia, None):
        
        
        if hora_hoy >= crea_hora(7, 30, 0): # no se puede reservar atencion para un mismo dia despues de las 7:30
            del semana[dia]
    
    return semana








### vistas llamadas mediante ajax ###

@login_required(login_url="auth:login")
def get_horas_disponibles(request):
    """
    Retorna el siguiente JSON:
    `{"opciones": opciones}`, donde opciones es una lista de diccionarios:
    `[{hora: lista de medicos disponibles}, ..., {hora: lista de medicos disponibles}]`

    - Si no hay horas disponibles, opciones es una lista vacía `[]`.
    - Si no hay médicos disponibles para una hora, dicha hora no es incluida en `opciones`.


    """

    # obtenemos la fecha en la que quiere reservar la atencion
    fecha = request.GET.get('fecha') #yyyy-mm-dd

    # obtenemos las atenciones de ese dia en particular
    atenciones_del_dia = Atencion.objects.filter(fecha_atencion=fecha)


    # vamos pregunta por cada horario los medicos disponibles
    opciones = []

    fecha_separada = fecha.split("-")
    horario = horarios_hosp.get_horario(
        calendar.weekday(
            year=int(fecha_separada[0]), 
            month=int(fecha_separada[1]), 
            day=int(fecha_separada[2]))
    )
    
    for hora in horario:        

        # Utilizamos exclude() en el modelo Medico para excluir aquellos médicos 
        # que tienen una atención programada a una determinada hora.
        atencion_con_hora_fecha = Atencion.objects.filter(hora_atencion=hora, fecha_atencion=fecha)
        medicos_con_atencion = atencion_con_hora_fecha.values_list('medico_id', flat=True)
        medicos_disponibles = Medico.objects.exclude(id__in=medicos_con_atencion)
        

        if medicos_disponibles.exists():
            # guardamos la lista de medicos junto con la hora
            opciones.append({"hora": hora, "medicos": list(medicos_disponibles.values_list("id", "nombre", "apellido"))})
            

    return JsonResponse({'opciones': opciones})






### vistas que procesan el guardado de la atencion y la respuesta al usuario ###

@login_required(login_url="auth:login")
def ingresar_atencion_medica(request):
    
    if request.method == "POST":
        # reunimos la información recibida por post.
        fecha_atencion = request.POST["fecha"]
        hora_atencion = request.POST["hora"]
        id_usuario_conectado = Usuario.objects.get(username=request.user.username).id
        id_medico = request.POST["medico"]
        fecha_reserva = get_fecha_hora_hoy()

        try:
            # intentamos ingresar la atencion dentro de la db.
            atencion_ingresada = Atencion.objects.create(
                fecha_atencion=fecha_atencion, 
                hora_atencion=hora_atencion, 
                fecha_reserva=fecha_reserva, 
                medico_id=id_medico, 
                usuario_id=id_usuario_conectado
            )
            
        except IntegrityError as err:
            print(err)
            contexto = {"error": True, "codigo": "001"}
        else:
            # si el ingreso fue exitoso y no ocurrio un error, entonces renderizamos 
            # la plantilla de exito con los datos de la reserva y enviamos un email 
            # de respaldo.
            
            medico = Medico.objects.get(id=id_medico) #datos del medico
            nombre_box = medico.box.nombre #nombre del box            

            contexto = {
                "id": atencion_ingresada.id,
                "rut": request.user.username,
                "email": request.user.email,
                "fecha": formatea_fecha(fecha_atencion),
                "hora": hora_atencion,
                "medico": f"{medico.nombre} {medico.apellido}",
                "box": nombre_box,
                "error": False,
            }
            
            enviar_email(contexto)

        return render(request, "hospital/respuesta_reserva_atencion.html", context=contexto)
    
    
    return redirect("hosp:reservar_atencion")



def enviar_email(contexto):
    """
    Envía email al usuario con la información de reserva.
    
    """
    
    subject = "Atención Reservada"
    message = ("Estimado/a\n\nLa reserva de atención médica fue exitosa." 
    "Muchas gracias por utilizar nuestra plataforma."
    "\n\nLa información de su reserva de atención es la siguiente:\n" 
    f"Id atención: {contexto['id']}\n"
    f"Rut: {contexto['rut']}\n"
    f"Email: {contexto['email']}\n"
    f"Fecha: {contexto['fecha']}\n"
    f"Hora: {contexto['hora']}\n"
    f"Médico: {contexto['medico']}\n"
    f"Box: {contexto['box']}\n")
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [contexto["email"]]

    send_mail(
        subject, message, email_from, recipient_list
    )











