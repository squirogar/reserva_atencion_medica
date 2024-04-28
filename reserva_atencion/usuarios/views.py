from django.conf import settings
from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CambioEmailForm, CambioDatosForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
# Create your views here.


@login_required(login_url="auth:login")
def perfil(request):
    # recuperar datos del usuario conectado
    perfil_usuario = {}
    if request.user.is_authenticated:
        username = request.user.username
        usuario = Usuario.objects.get(username=username)
        print(f"usuario {usuario}")
        perfil_usuario["usuario"] = usuario
        
        perfil_usuario["form_cambio_datos"] = CambioDatosForm(instance=request.user)
        perfil_usuario["form_cambio_email"] = CambioEmailForm(instance=request.user)
        perfil_usuario["form_cambio_password"] = PasswordChangeForm(user=request.user)

    return render(request, "usuarios/perfil.html", context=perfil_usuario)



@login_required(login_url="auth:login")
def cambia_password(request):
    form = PasswordChangeForm(user=request.user)
    cambio_efectivo = None
    mensajes = None

    if request.method == 'POST':
        #passwordchangeform recibe el usuario y la data enviada por post
        #esto es para validar que la contraseña le pertenezca al usuario
        #conectado
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # esto es para que el usuario no deba loguearse al cambiar la contraseña
            update_session_auth_hash(request, form.user)
            
            cambio_efectivo = True

            
        else:
            cambio_efectivo = False
            mensajes = form.errors
        
        return JsonResponse({"cambio_efectivo": cambio_efectivo, "mensajes": mensajes})

    return redirect("usr:perfil")
    #return render(request, 'usuarios/cambia_password.html', context={"form": form,})




@login_required(login_url="auth:login")
def cambia_datos(request):
    cambio_efectivo = None
    datos = {}
    mensajes = None

    if request.method == "POST":
        form = CambioDatosForm(data=request.POST, instance=request.user)
        if form.is_valid():

            print("save")
            form.save()
            cambio_efectivo = True
            datos["nombre"] = form.cleaned_data["first_name"]
            datos["apellido"] = form.cleaned_data["last_name"]
            datos["direccion"] = form.cleaned_data["direccion"]

        else:
            cambio_efectivo = False
            mensajes = form.errors
        return JsonResponse({"cambio_efectivo": cambio_efectivo, "datos": datos, "mensajes": mensajes})
    
    return redirect("usr:perfil")



@login_required(login_url="auth:login")
def cambia_email(request):
    cambio_efectivo = False
    mensaje = None
    datos = None
    email_antiguo = request.user.email
    
    if request.method == "POST":
        form = CambioEmailForm(data=request.POST, instance=request.user)
        if form.is_valid():
            email_nuevo = form.cleaned_data["email"]
            print("save")
            form.save()
            cambio_efectivo = True
            mensaje = "Éxito"
            datos = {"email": email_nuevo}

            send_mail(
                subject="Cambio de email", 
                message=(f"Estimado/a\n\nUsted ha cambiado su email de {email_antiguo} a {email_nuevo}\n"
                         f"Si tiene una duda respecto, comuníquese con nosotros en nuestra plataforma."),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email_antiguo, email_nuevo]
            )

        else:
            mensaje = form.errors

        return JsonResponse({"cambio_efectivo": cambio_efectivo, "mensaje": mensaje, "datos": datos})
    
    return redirect("usr:perfil")