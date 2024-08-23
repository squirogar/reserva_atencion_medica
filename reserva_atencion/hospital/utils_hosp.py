#utils_hosp.py
from django.utils import timezone
from datetime import date, time

def get_fecha_hora_hoy():

    # timezone.now() devuelve la fecha y hora del día de hoy
    # pero en UTC, para pasarla a la hora correcta del país
    # se debe usar timezone.localtime()
    return timezone.localtime(timezone.now())


def crea_fecha(year, month, day):
    """
    Devuelve un objeto datetime.date con los datos indicados
    """
    return date(year, month, day)


def formatea_fecha(fecha):
    """
    Recibe un string que representa una fecha.
    Devuelve un string representando una fecha en formato (dd-mm-yyyy).
    """
    return date.fromisoformat(fecha).strftime("%d-%m-%Y")


def crea_hora(hour, min, sec):
    """
    Recibe 3 enteros: hora, minuto y segundo.
    devuelve un objeto datetime.time
    """
    return time(hour, min, sec)