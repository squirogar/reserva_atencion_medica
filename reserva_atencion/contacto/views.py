from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import FormularioContacto

# Create your views here.

@login_required(login_url="auth:login")
def contacto(request):
    formulario = FormularioContacto()
    
    if request.method == "POST": 
        formulario = FormularioContacto(data=request.POST)

        if formulario.is_valid():
            subject = "Mensaje de " + formulario.cleaned_data["nombre"]
            message = formulario.cleaned_data["contenido"] + " " + formulario.cleaned_data["email"]
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]


            send_mail(subject, message, email_from, recipient_list)
            
            messages.success(request, "Mensaje recibido. Gracias")

    return render(request, "contacto/contacto.html", {"formulario": formulario})