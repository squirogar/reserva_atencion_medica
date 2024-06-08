
class ReservaAtencionRouter:
    """
    Un router para controlar todas las operaciones de las dos
    bases de datos: feriados y default.

    - default: alias de la base de datos "reserva_atencion".  
    - feriados_db: alias base de datos "feriados". Sólo lectura.
    Sólo los modelos de la app "feriados" deben interactuar
    con esta base de datos.
    """

    
    
    def db_for_read(self, model, **hints):
        """
        Los intentos de leer modelos de la app "feriados"
        van a "feriados_db".
        """
        if model._meta.app_label == "feriados":
            return "feriados_db"
        return "default"


    def db_for_write(self, model, **hints):
        """
        Los intentos de escribir modelos de las apps van
        a la base de datos "default".
        La base de datos "feriados_db" será de sólo
        lectura.
        """
        if model._meta.app_label != "feriados":
            return "default"

        return None



    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones si:
        - los dos modelos son parte de la app "feriados"
        - los dos modelos no son parte de la app "feriados"
        """

        if obj1._meta.app_label == "feriados" and obj2._meta.app_label == "feriados":
            return True
        elif "feriados" not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return None
        

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegura que la migración solo se aplique en las bases de datos correctas.
        Sólo se permite la migración de apps distintas de "feriados" y que la
        base de datos a migrar sea "default".
        """
        if app_label != "feriados":
            return db == "default"
        return False