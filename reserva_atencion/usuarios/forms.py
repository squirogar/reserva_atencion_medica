# forms.py
from django import forms
#from django.contrib.auth.forms import UserChangeForm
from .models import Usuario


class CambioDatosForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name = forms.CharField(label="Apellido", max_length=150, required=True)
    direccion = forms.CharField(label="Dirección", max_length=300, required=True)

    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "direccion")




class CambioEmailForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ("email",)

