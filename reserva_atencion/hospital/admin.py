from django.contrib import admin
from .models import *



class AtencionAdmin(admin.ModelAdmin):
    #list_display = ("nombre", "direccion", "telefono")
    list_filter = ("usuario", "medico", "fecha_atencion", "hora_atencion")



# Register your models here.
admin.site.register(Medico)
admin.site.register(Box)
admin.site.register(Atencion, AtencionAdmin)