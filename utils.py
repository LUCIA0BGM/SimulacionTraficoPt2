import random

ANCHO, ALTO = 800, 600
COLOR_FONDO = (30, 30, 30)
COLOR_CALLE = (70, 70, 70)
COLOR_VEHICULO = (0, 200, 255)
COLOR_SEMAFORO = {
    "rojo": (255, 0, 0),
    "verde": (0, 255, 0)
}


def generar_spawn_aleatorio(nombre_zona):
    if nombre_zona.lower().endswith("norte"):
        posibles_origenes = ["NORTE", "ESTE", "OESTE"]
    else:
        posibles_origenes = ["SUR", "ESTE", "OESTE"]

    origen = random.choice(posibles_origenes)

    if origen == "NORTE":
        return [random.choice([290, 390, 490]), 0], "SUR"
    elif origen == "SUR":
        return [random.choice([290, 390, 490]), 580], "NORTE"
    elif origen == "ESTE":
        return [800, random.choice([190, 290, 390])], "OESTE"
    elif origen == "OESTE":
        return [0, random.choice([190, 290, 390])], "ESTE"
