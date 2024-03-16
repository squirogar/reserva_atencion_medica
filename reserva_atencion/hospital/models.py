from django.db import models
from django.core.validators import MinLengthValidator
from usuarios.models import Usuario
# Create your models here.

class Medico(models.Model):
    rut = models.CharField(max_length=10, validators=[MinLengthValidator(10)], unique=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    especialidad = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="hospital/medicos", null=True, blank=True)

    class Meta:
        db_table = "medicos"
        verbose_name = "medico"
        verbose_name_plural = "medicos"


    def __str__(self):
        return self.nombre_completo



class AtencionMedica(models.Model):
    dia = models.CharField(max_length=9)
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    box = models.CharField(max_length=50)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    usuario = models.ManyToManyField(Usuario, through="ReservaAtencion")

    class Meta:
        db_table = "atencion_medica"
        verbose_name = "atencion medica"
        verbose_name_plural = "atenciones medica"

    def __str__(self):
        return f"{self.dia}, {self.hora_inicio}-{self.hora_termino}, box: {self.box}, dr: {self.medico}"



class ReservaAtencion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    atencionmedica = models.ForeignKey(AtencionMedica, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "reserva_atencion"
        verbose_name = "reserva de atencion"
        verbose_name_plural = "reservas de atencion"