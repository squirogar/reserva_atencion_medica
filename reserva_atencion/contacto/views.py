from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import FormularioContacto
from django.contrib import messages

# Create your views here.

#@login_required(login_url="auth:login")
def contacto(request):
    formulario = FormularioContacto()
    
    if request.method == "POST": 
        formulario = FormularioContacto(data=request.POST)

        if formulario.is_valid():
            enviar_email(formulario)

            messages.success(request, "Mensaje recibido. Gracias")
            return redirect("cont:contacto")

    return render(request, "contacto/contacto.html", {"formulario": formulario})



def enviar_email(formulario):
    # al correo de la aplicacion
    send_mail(
        subject="Mensaje de " + formulario.cleaned_data["nombre"], 
        message=formulario.cleaned_data["contenido"] + "\n\n" + formulario.cleaned_data["email"], 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[settings.EMAIL_HOST_USER]
    )

    # al correo del usuario
    send_mail(
        subject="Mensaje recibido", 
        message=" Estimado/a " 
        + formulario.cleaned_data["nombre"] 
        + "\n\nMuchas gracias por su mensaje. Su retroalimentación nos ayuda a mejorar\n"
        + "El asunto será analizado y resuelto a la brevedad.\n\nEquipo de desarrollo.", 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[formulario.cleaned_data["email"]]
    )

