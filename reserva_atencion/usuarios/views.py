from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CambioEmailForm, CambioDatosForm
from django.contrib import messages
from django.http import JsonResponse
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

    if request.method == 'POST':
        #passwordchangeform recibe el usuario y la data enviada por post
        #esto es para validar que la contraseña le pertenezca al usuario
        #conectado
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # esto es para que el usuario no deba loguearse al cambiar la contraseña
            update_session_auth_hash(request, form.user)
            
            messages.success(request, "Éxito")
            
        else:
            messages.error(request, form.errors)

    return redirect("usr:perfil")
    #return render(request, 'usuarios/cambia_password.html', context={"form": form,})




@login_required(login_url="auth:login")
def cambia_datos(request):

    if request.method == "POST":
        form = CambioDatosForm(data=request.POST, instance=request.user)
        if form.is_valid():

            messages.success(request, "Éxito")
            
            print("save")
            form.save()
        else:
            messages.error(request, form.errors)

    return redirect("usr:perfil")



@login_required(login_url="auth:login")
def cambia_email(request):

    cambio_efectivo = False
    mensaje = None
    datos = None
    if request.method == "POST":
        form = CambioEmailForm(data=request.POST, instance=request.user)
        if form.is_valid():

            print("save")
            form.save()
            cambio_efectivo = True
            mensaje = "Éxito"
            datos = {"email": form.cleaned_data["email"]}

        else:
            mensaje = form.errors

    return JsonResponse({"cambio_efectivo": cambio_efectivo, "mensaje": mensaje, "datos": datos})