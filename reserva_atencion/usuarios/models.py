from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.

class Usuario(AbstractUser):
    # campos adicionales
    username = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    direccion = models.CharField(max_length=300)
    
    # redefinimos el email para que sea unique
    email = models.EmailField(max_length=100, unique=True)

    class Meta:
        db_table = "usuarios"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    
    def __str__(self):
        return self.username
