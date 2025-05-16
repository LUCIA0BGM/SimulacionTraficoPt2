
class Interseccion:
    def __init__(self, posicion):
        self.posicion = posicion
        self.semaforo = None

    def asignar_semaforo(self, semaforo):
        self.semaforo = semaforo
