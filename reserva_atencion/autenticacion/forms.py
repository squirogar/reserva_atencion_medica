import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from usuarios.models import Usuario

class UserCreationFormulario(UserCreationForm):
    username = forms.CharField(
        label="Rut", max_length=10, min_length=10, required=True, 
        help_text=("El rut debe ser de longitud 10, con guión y dígito verificador"))
    first_name = forms.CharField(label="Nombre", max_length=150, required=True)
    last_name = forms.CharField(label="Apellido", max_length=150, required=True)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    direccion = forms.CharField(label="Dirección", max_length=300, required=True)

    class Meta:
        model = Usuario
        fields = ("username", "email", "first_name", "last_name", "direccion", "password1", "password2")
        

    def __init__(self, *args, **kwargs):
        super(UserCreationFormulario, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = '123456789-0'
        self.fields['email'].widget.attrs['placeholder'] = 'user@gmail.com'
        self.fields['direccion'].widget.attrs['placeholder'] = 'calle 123 pasaje x casa 1'


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


    def clean_username(self):
        """
        clean() llama a este método para verificar que username (rut en este caso)
        cumple con el formato.

        Puede usarse para cualquier campo, usar: clean_campo().
        """
        rut = self.cleaned_data["username"]

        print(type(rut))

        match = re.fullmatch(r"^\d{8}-[\dk]$", rut)

        print("re: ", match)
        
        if not match:
            raise forms.ValidationError("El rut debe ser de longitud 10, con guión y dígito verificador")

        
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return rut


class LoginFormulario(AuthenticationForm):

    error_messages = {
        'invalid_login': ("Por favor ingresar un rut y/o contraseña correctos. "
                           "Note que ambos campos pueden ser sensibles a mayúsculas."),
        'inactive': ("Cuenta inactiva."),
    }
    

    def __init__(self, *args, **kwargs):
        super(LoginFormulario, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = '12345678-9'
        self.fields["username"].label = "Rut"
    

    def clean_username(self):
        """
        clean() llama a este método para verificar que username (rut en este caso)
        cumple con el formato.

        Puede usarse para cualquier campo, usar: clean_campo().
        """
        rut = self.cleaned_data["username"]

        print(type(rut))

        match = re.fullmatch(r"^\d{8}-[\dk]$", rut)

        print("re: ", match)
        
        if not match:
            raise forms.ValidationError("El rut debe ser de longitud 10, con guión y dígito verificador")

        
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return rut
    
