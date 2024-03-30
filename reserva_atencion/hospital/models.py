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
    usuario = models.ManyToManyField(Usuario, blank=True, through="Atencion")

    class Meta:
        db_table = "medicos"
        verbose_name = "medico"
        verbose_name_plural = "medicos"


    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Box(models.Model):
    nombre = models.CharField(max_length=10)
    medico = models.OneToOneField(Medico, on_delete=models.CASCADE)

    class Meta:
        db_table = "boxes"
        verbose_name = "box"
        verbose_name_plural = "boxes"

    def __str__(self):
        return self.nombre


class Atencion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_atencion = models.DateField()
    hora_atencion = models.TimeField()

    fecha_reserva = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "atencion"
        verbose_name = "atencion"
        verbose_name_plural = "atenciones"
        constraints = [
            models.UniqueConstraint(fields=["medico", "fecha_atencion", "hora_atencion"], name="unique_reserva_atencion")
        ]

    def __str__(self):
        return f"{self.usuario}, {self.medico}, {self.fecha_atencion}, {self.hora_atencion}"

