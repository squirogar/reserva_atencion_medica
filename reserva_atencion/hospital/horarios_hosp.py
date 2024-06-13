# horarios_hosp.py

def get_horario(dia):
    """
    Retorna una lista con el horario de trabajo dependiendo del día.

    Args:
    - dia (int): número de 0-6. Si dia es 4, es día viernes y,
    por lo tanto, el horario es hasta las 16:00 hrs.

    Returns:
    - lista de strings con las horas de atención disponibles.
    """
    horario = [
        "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", 
        "11:00", "11:30", "12:00", "14:00", "14:30", 
        "15:00", "15:30", "16:00"
    ]

    print(dia)

    if dia == 5 or dia == 6:
        raise ValueError("Horario no disponible para sabados o domingos")

    elif dia == 4:
        return horario

    else:
        horario.extend(["16:30"])
        return horario
    