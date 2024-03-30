from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Usuario

class UserCreationFormulario(UserCreationForm):
    username = forms.CharField(label="Rut", max_length=10, min_length=10, required=True)
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name = forms.CharField(label="Apellido", max_length=150, required=True)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    direccion = forms.CharField(label="Dirección", max_length=300, required=True)

    class Meta:
        model = Usuario
        fields = ("username", "email", "first_name", "last_name", "direccion", "password1", "password2")
        

    def save(self, commit=True):
        """
        Redefine el método save, para que evite guardar inmediatamente los
        datos del usuario nuevo en la base de datos.
        Este método guardará los campos username (rut), contraseña, email,
        direccion.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.direccion = self.cleaned_data["direccion"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user