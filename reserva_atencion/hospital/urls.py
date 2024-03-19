from django.urls import path
from . import views

urlpatterns = [
    path("historial/", views.historial, name="historial"),
    path("reservar/", views.reservar_atencion, name="reservar_atencion"),
    path("medicos/", views.medicos, name="medicos"),
]