# simulacion_trafico/environment/vehicle.py

class Vehicle:
    def __init__(self, id_, position, speed, direction):
        self.id = id_
        self.position = list(position)
        self.speed = speed
        self.direction = direction
        self.en_espera = False  # Si está esperando por semáforo

    def mover(self, city):
        if self.debe_detenserse(city):
            self.en_espera = True
            return

        self.en_espera = False
        if self.direction == "NORTE":
            self.position[1] -= self.speed
        elif self.direction == "SUR":
            self.position[1] += self.speed
        elif self.direction == "ESTE":
            self.position[0] += self.speed
        elif self.direction == "OESTE":
            self.position[0] -= self.speed

    def debe_detenserse(self, city):
        for interseccion in city.intersecciones:
            semaforo = interseccion.semaforo
            if not semaforo:
                continue
            x, y = self.position
            sx, sy = semaforo.position

            distancia = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
            if distancia < 2.0 and semaforo.state != "verde":
                return True
        return False
