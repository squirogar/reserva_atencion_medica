from django.urls import path
from . import views

urlpatterns = [
    path("historial/", views.historial, name="historial"),
    path("reservar/", views.reservar_atencion, name="reservar_atencion"),
    path("medicos/", views.medicos, name="medicos"),
    path('get_horas_disponibles/', views.get_horas_disponibles, name='get_horas_disponibles'),
    path('resultado/', views.ingresar_atencion_medica, name='ingresar_atencion_medica'),
]
