class DiaAtencion():
    def __init__(self, dia, fecha, lista_horas):
        self.dia = dia
        self.fecha = fecha
        self.lista_horas = lista_horas

    def get_dia(self):
        return self.dia
    
    def get_fecha(self):
        return self.fecha

    def get_lista_hora(self):
        return self.lista_horas



class Hora():
    def __init__(self, hora, medicos):
        self.hora = hora
        self.medicos = medicos
    
    def get_hora(self):
        return self.hora
    
    def get_medicos(self):
        return self.medicos