from django.urls import path
from . import views

urlpatterns = [
    path("historial/", views.historial, name="historial"),
    path("reservar/", views.reservar_hora, name="reservar_hora"),
    path("medicos/", views.medicos, name="medicos"),
]