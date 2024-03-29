from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def ingresar(request):
    form = AuthenticationForm()
    if request.method == "POST":
        # guardamos la data enviada por el usuario
        form = AuthenticationForm(request, request.POST)

        # si el formulario es valido
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            print(username, password)

            # comparamos con la info que está en la bd
            usuario = authenticate(username=username, password=password)

            print(usuario)

            # si es correcta la info, entonces usuario != None
            if usuario is not None:
                login(request, usuario)
                return redirect("reservar_atencion")
            else:
                #messages.error(request, "Error: No se encuentra el usuario")
                print("error")
                
        else:
            #messages.error(request, "Error: Datos incorrectos")
            print("error")
            

    return render(request, "login.html", context={"form": form})






def registro(request):
    return render(request, "registro.html")







@login_required(login_url="auth:login")
def cerrar_sesion(request):
    logout(request)
    return redirect("auth:login")