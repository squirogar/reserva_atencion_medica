# forms.py
from django import forms
#from django.contrib.auth.forms import UserChangeForm
from .models import Usuario
import regex


class CambioDatosForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name = forms.CharField(label="Apellido", max_length=150, required=True)
    direccion = forms.CharField(label="Dirección", max_length=300, required=True)

    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "direccion")
    
    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]

        match = regex.fullmatch(r"^\p{L}+$", first_name)

        print("re: ", match)
        
        if not match:
            raise forms.ValidationError("El nombre solo debe contener letras.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]

        match = regex.fullmatch(r"^\p{L}+$", last_name)

        print("re: ", match)
        
        if not match:
            raise forms.ValidationError("El apellido solo debe contener letras.")

        return last_name



class CambioEmailForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ("email",)

    def clean_email(self):
        usuario = self.instance
        email = self.cleaned_data["email"]
        print("usuario email ", usuario.email)
        print("usuario nuevo email ", email)

        if usuario.email == email:
            print("iguales")
            raise forms.ValidationError("El email nuevo debe ser diferente al que ya tiene registrado")

        return email

