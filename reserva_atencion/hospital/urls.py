from django.urls import path
from . import views

urlpatterns = [
    path("historial/", views.historial, name="historial"),
    path("reservar/", views.reservar_atencion, name="reservar_atencion"),
    path("medicos/", views.medicos, name="medicos"),
    path('get_horas_disponibles/', views.get_horas_disponibles, name='get_horas_disponibles'),
    path('get_medicos_disponibles/', views.get_medicos_disponibles, name='get_medicos_disponibles'),
    path('reserva_atencion_medica/', views.reserva_atencion_medica, name='reserva_atencion_medica'),
]
