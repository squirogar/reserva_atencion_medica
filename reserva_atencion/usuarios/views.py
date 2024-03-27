from django.shortcuts import render
from .models import Usuario
from django.contrib.auth.decorators import login_required
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

    return render(request, "perfil.html", context=perfil_usuario)