from django.urls import path
from . import views

app_name = "auth"

urlpatterns = [
    path("login/", views.ingresar, name="login"),
    path("registro/", views.registro, name="registro"),
    path("logout/", views.cerrar_sesion, name="cerrar_sesion"),
]
