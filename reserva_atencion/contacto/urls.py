from django.urls import path
from . import views

app_name = "cont"

urlpatterns = [
    path("", views.contacto, name="contacto"),
]