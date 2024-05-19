import re
import regex
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from usuarios.models import Usuario

class UserCreationFormulario(UserCreationForm):
    username = forms.CharField(
        label="Rut", max_length=10, min_length=10, required=True, 
        help_text=("Su rut debe ser de longitud 10, con guión y dígito verificador")
    )
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

        self.fields['username'].error_messages.update({
            "unique": "Ya existe otro usuario registrado con ese rut.",
        })
        

    def save(self, commit=True):
        """
        Redefine el método save de UserCreationForm.
        Este método guardará los campos username (rut), contraseña, email,
        direccion, además de los que ya se guardan por defecto.
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

        # validamos que cumpla con el formato requerido
        match = re.fullmatch(r"^\d{8}-[\dk]$", rut)

        print("re: ", match)
        
        if not match:
            raise forms.ValidationError("El rut debe ser de longitud 10, con guión y dígito verificador")
        

        # validamos que sea un rut válido
        if not self.valida_rut(rut):
            raise forms.ValidationError("El rut ingresado no es válido.")

        
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return rut


    def valida_rut(self, rut):
        """
        Realiza la comprobación de que el rut sea válido utilizando
        el algoritmo del módulo 11.

        retorna True si el rut especificado es válido, de lo contrario
        se retorna False.
        """

        RUT = rut.lower()
        digitos = RUT.split("-")[0]
        # se debe invertir el orden de los dígitos del rut
        digitos = digitos[::-1]
        
        FACTORES = [2, 3, 4, 5, 6, 7, 2, 3]
        resultados = []

        # se multiplica cada dígito por su factor ponderado
        for digito, factor in zip(digitos, FACTORES):
            resultados.append(int(digito) * factor)
        
        suma = sum(resultados)
        resto = suma % 11

        # asignamos el dígito verificador del rut de acuerdo
        # al resultado final de la operación
        resultado_final = 11 - resto
        digito_verificador = -1

        if resultado_final < 10:
            digito_verificador = resultado_final
        elif resultado_final == 10:
            digito_verificador = "k"
        elif resultado_final == 11:
            digito_verificador = 0

        # Comprobamos que el dígito verificador del rut 
        # ingresado sea el mismo que el calculado por el
        # algoritmo del módulo 11
        ultimo_digito = RUT[-1] # string

        if (ultimo_digito != "k"):
            ultimo_digito = int(ultimo_digito)

        if ultimo_digito == digito_verificador:
            return True
        else:
            return False




        




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
    
