from django.urls import path
from . import views

app_name = "usr"
urlpatterns = [
    path("", views.perfil, name="perfil"),
    path("cambiar_password/", views.cambia_password, name="cambia_password"),
    path("cambiar_email/", views.cambia_email, name="cambia_email"),
    path("cambiar_datos/", views.cambia_datos, name="cambia_datos"),
]