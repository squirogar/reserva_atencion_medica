# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Feriados(models.Model):
    # TIPO_CHOICES = [(valor_en_db, valor_en_formulario)]
    RELIGIOSO = "Religioso"
    CIVIL = "Civil"

    TIPO_CHOICES = [
        (RELIGIOSO, "Religioso"),
        (CIVIL, "Civil"),
    ]

    fecha = models.DateField(unique=True)
    motivo = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=9,
        choices=TIPO_CHOICES,
    )

    class Meta:
        managed = False
        db_table = "feriados"
    

    def __str__(self):
        return f"{self.fecha} - {self.motivo} ({self.tipo})"
