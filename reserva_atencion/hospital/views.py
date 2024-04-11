from django.shortcuts import render, redirect
from .models import Medico, Atencion, Box
from usuarios.models import Usuario
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail
from django.conf import settings

from datetime import date
import calendar
import locale
from django.utils import timezone

from django.db import IntegrityError


# Create your views here.

# cambiamos el locale para que los dias de semana sean en español
locale.setlocale(locale.LC_ALL, 'es_Es')



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


###


@login_required(login_url="auth:login")
def reservar_atencion(request):
    print("\n\nvista Reservar_atencion:\n")
    
    contexto = {}
    
    # preguntamos si el usuario puede reservar atencion
    if habilitado_para_reservar(request.user.username):

        # obtenemos los días restantes de la semana
        dia_de_hoy = timezone.localdate(timezone.now()) #date.today()
        print("dia de hoy", dia_de_hoy)
        fechas_semana = get_semana(dia_de_hoy.year, dia_de_hoy.month, dia_de_hoy.day)
        print("-fechas_semana: ", fechas_semana, "\n")

        fechas_semana = limpia_semana(fechas_semana)


        contexto["hoy"] = fechas_semana["hoy"]
        contexto["semana"] = fechas_semana["semana"]
        contexto["error"] = False
        
    else:
        contexto["error"] = True

    return render(request, "hospital/reservar_atencion.html", context=contexto)





def limpia_semana(semana):
    # eliminamos sabado y domingo
    del semana["sábado"]
    del semana["domingo"]

    print("semana luego de la eliminacion ", semana)

    # si consideramos el dia de hoy para pedir hora
    hoy = timezone.localtime(timezone.now())
    hora_hoy = hoy.time().strftime("%H:%M")    

    numero_dia_hoy = calendar.weekday(hoy.year, hoy.month, hoy.day) # numero_dia actual: [0-6]
    dia = calendar.day_name[numero_dia_hoy] # dia de la semana que es hoy

    print(numero_dia_hoy, dia)

    if semana.get(dia, None): # se verifica que hoy no sea domingo, ya que domingo no se atiende
        if hora_hoy >= "7:30": # no se puede reservar atencion para un mismo dia despues de las 7:30
            del semana["dia"]
    
    return semana



def habilitado_para_reservar(usuario):
    """
    Retorna True si el usuario conectado puede reservar una atencion.
    Caso contrario, retorna False.

    Un usuario no puede reservar una atención si: 
    - si es sábado, o domingo antes de las 17:00
    - si ya reservó una atención para la semana actual y dicha reserva
    aún no expira (fecha y hora de hoy <= fecha y hora de atencion).
    Por ejemplo, si el usuario reserva para un día martes a las 8:00,
    a partir de las 8:01 de ese martes puede volver a reservar.

    Con esto se evita que un usuario pueda hacer múltiples reservas.
    
    """
    print("\nHabilitado para reservar\n")

    hoy = timezone.localtime(timezone.now())
    hora_hoy = hoy.time().strftime("%H:%M")
    
    dia_semana = calendar.weekday(hoy.year, hoy.month, hoy.day) # [0-6]
    
    # si es sabado, o (domingo y la hora < 17:00)
    if dia_semana == 5 or (dia_semana == 6 and hora_hoy < "17:00"): 
        return False

    # comprobamos si el usuario ya tiene una reserva activa, o sea,
    # aun no expira la reserva de atencion.
    id_usuario_conectado = Usuario.objects.get(username=usuario).id
    print("id_usuario ", id_usuario_conectado)

    atenciones_usuario_conectado = Atencion.objects.filter(usuario_id=id_usuario_conectado)
    print(atenciones_usuario_conectado)

    if atenciones_usuario_conectado: # si tiene atenciones
        ultima_atencion_reservada = atenciones_usuario_conectado.latest("fecha_reserva")
        
        #### borrar #####
        print("ultima atencion usuario", ultima_atencion_reservada)
        #print("fecha recuperada por django", ultima_atencion.fecha_reserva, type(ultima_atencion.fecha_reserva))
        #print("fecha con localdate ", timezone.localtime(ultima_atencion.fecha_reserva))

        #print(ultima_atencion.fecha_reserva.year, ultima_atencion.fecha_reserva.month, ultima_atencion.fecha_reserva.day)
        #print(ultima_atencion.fecha_reserva.date(), type(ultima_atencion.fecha_reserva.date()))
        #print("date.today()", date.today(), "localdate(timezone.now())", timezone.localdate(timezone.now()))

        fecha_atencion_ultima_reserva = ultima_atencion_reservada.fecha_atencion
        hora_atencion_ultima_reserva = ultima_atencion_reservada.hora_atencion

        print(fecha_atencion_ultima_reserva, hora_atencion_ultima_reserva, hoy.date(), hoy.time())
        ##########

        # preguntamos si aun no ha expirado la reserva
        hora_hoy = hoy.time().replace(microsecond=0)

        if hoy.date() < fecha_atencion_ultima_reserva: 
            return False
        elif hoy.date() == fecha_atencion_ultima_reserva and hora_hoy <= hora_atencion_ultima_reserva:
            return False
        else:
            return True
        #if timezone.localdate(timezone.now()) == fecha_ultima_reserva: # si ya hizo una reserva hoy
        #if date.today() == ultima_atencion.fecha_reserva.date(): # si ya hizo una reserva hoy
        #    print("iguales")
        #    return False
        
    return True





from django.http import JsonResponse

@login_required(login_url="auth:login")
def get_horas_disponibles(request):
    """
    Retorna el siguiente JSON:
    `{"opciones": opciones}`, donde opciones es una lista de diccionarios:
    `[{hora: lista de medicos disponibles}, ..., {hora: lista de medicos disponibles}]`

    - Si no hay horas disponibles, opciones es una lista vacía `[]`.
    - Si no hay médicos disponibles para una hora, dicha hora no es incluida en `opciones`.


    """
    print("se llamo a get_horas_disponibles")
    print("\nHORAS DISPONIBLES AJAX")

    # obtenemos la fecha en la que quiere reservar la atencion
    fecha = request.GET.get('fecha')
    print(fecha)

    # obtenemos las atenciones de ese dia en particular
    atenciones_del_dia = Atencion.objects.filter(fecha_atencion=fecha)
    print(atenciones_del_dia, "\n")


    # vamos pregunta por cada horario los medicos disponibles
    opciones = []
    horarios= [
            "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30",
            "12:00", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30"
        ]
    
    
    for hora in horarios:
        print("\t hora", hora)

        # el viernes solo se trabaja hasta las 16:00
        

        # Utilizamos exclude() en el modelo Medico para excluir aquellos médicos 
        # que tienen una atención programada a una determinada hora.
        atencion_con_hora_fecha = Atencion.objects.filter(hora_atencion=hora, fecha_atencion=fecha)
        medicos_con_atencion = atencion_con_hora_fecha.values_list('medico_id', flat=True)
        medicos_disponibles = Medico.objects.exclude(id__in=medicos_con_atencion)

        print("medicos disponibles: ", medicos_disponibles)
        print(list(medicos_disponibles.values_list("id", "nombre", "apellido")))
        

        if medicos_disponibles:
            # guardamos la lista de medicos junto con la hora
            opciones.append({"hora": hora, "medicos": list(medicos_disponibles.values_list("id", "nombre", "apellido"))})
            

    return JsonResponse({'opciones': opciones})








@login_required(login_url="auth:login")
def ingresar_atencion_medica(request):
    
    print("\n\nse llamo a ingresar_atencion_medica")

    if request.method == "POST":
        # reunimos la información recibida por post.
        fecha_atencion = request.POST["fecha"]
        hora_atencion = request.POST["hora"]
        id_usuario_conectado = Usuario.objects.get(username=request.user.username).id
        id_medico = request.POST["medico"]
        fecha_reserva = timezone.localtime(timezone.now()) #date.today()

        print("datos antes de la insercion")
        print(fecha_atencion, hora_atencion, id_usuario_conectado, id_medico, fecha_reserva)

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
            contexto = {"error": True}
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
                "fecha": date.fromisoformat(fecha_atencion).strftime("%d-%m-%Y"),
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


    info_semana["hoy"] = date(year, month, day)
    info_semana["semana"] = semana

    return info_semana






@login_required(login_url="auth:login")
def medicos(request):
    # se recuperan todos los medicos y los boxes donde trabajan
    medicos_con_box = Medico.objects.select_related("box")

    lista_medicos = {"medicos": medicos_con_box}

    return render(request, "hospital/medicos.html", lista_medicos)