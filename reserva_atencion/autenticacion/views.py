from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from autenticacion.forms import UserCreationFormulario, LoginFormulario
from django.contrib import messages


# Create your views here.



def ingresar(request):
    form = LoginFormulario()#AuthenticationForm()
    if request.method == "POST":
        # guardamos la data enviada por el usuario
        form = LoginFormulario(request, request.POST)#AuthenticationForm(request, request.POST)


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
                return redirect("home")
        """
            else:
                messages.error(request, "Error: No se encuentra el usuario")
                print("error")
                
        else:
            messages.error(
                request, 
                "Error: Datos incorrectos."
            )
            print("error")
        """    

    return render(request, "autenticacion/login.html", context={"form": form})






def registro(request):
    form = UserCreationFormulario()

    if request.method == "POST":
        print(request.POST)
        form = UserCreationFormulario(request.POST)
        if form.is_valid():
            # si el formulario es valido guardalo en la base de datos  
            usuario = form.save() 

            # si se guarda en la bd, redirige al usuario y
            # loguea automaticamente al usuario recien registrado
            login(request, usuario)

            return redirect("home")
        else:
            messages.error(request, "Error: los datos ingresados presentan errores.")
            print("error")

    return render(request, "autenticacion/registro.html", context={"form":form})







@login_required(login_url="auth:login")
def cerrar_sesion(request):
    logout(request)
    return redirect("auth:login")



