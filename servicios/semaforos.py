# servicios/semaforos.py

import pygame

COLOR_SEMAFORO = {"rojo": (255, 0, 0), "verde": (0, 255, 0)}

class Semaforo:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.direccion = direccion  # "horizontal" o "vertical"
        self.estado = "rojo"
        self.tiempo = 0

    def actualizar(self):
        self.tiempo += 1
        if self.tiempo >= 100:
            self.estado = "verde" if self.estado == "rojo" else "rojo"
            self.tiempo = 0

    def dibujar(self, ventana):
        color = COLOR_SEMAFORO[self.estado]
        offset = 15
        if self.direccion == "horizontal":
            pygame.draw.circle(ventana, color, (self.x, self.y - offset), 8)
        else:
            pygame.draw.circle(ventana, color, (self.x - offset, self.y), 8)

    def permite_pasar(self, vehiculo):
        if self.direccion == "horizontal" and vehiculo.dir in ["ESTE", "OESTE"]:
            return self.estado == "verde"
        elif self.direccion == "vertical" and vehiculo.dir in ["NORTE", "SUR"]:
            return self.estado == "verde"
        return True
