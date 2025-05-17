import asyncio
import pygame
import threading
import queue
import random
from comunicacion.mensajeria import recibir_vehiculos

ANCHO, ALTO = 800, 600
COLOR_FONDO = (30, 30, 30)
COLOR_CALLE = (70, 70, 70)
COLOR_VEHICULO = (0, 200, 255)
COLOR_SEMAFORO = {"rojo": (255, 0, 0), "verde": (0, 255, 0)}

# Definición de límites de la zona Norte
LIMITE_NORTE = 0
LIMITE_SUR = 600
LIMITE_OESTE = 0
LIMITE_ESTE = 800

class Semaforo:
    def __init__(self, x, y, direccion):
        self.x = x
        self.y = y
        self.direccion = direccion
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

class VehiculoSimulado:
    def __init__(self, id_, pos, dir_, vel):
        self.id = id_
        self.pos = list(pos)
        self.dir = dir_
        self.vel = vel

    def mover(self, semaforos):
        for s in semaforos:
            if s.permite_pasar(self):
                continue
            if self.dir == "SUR" and abs(self.pos[1] - s.y) < 10 and abs(self.pos[0] - s.x) < 20:
                return
            if self.dir == "NORTE" and abs(self.pos[1] - s.y) < 10 and abs(self.pos[0] - s.x) < 20:
                return
            if self.dir == "ESTE" and abs(self.pos[0] - s.x) < 10 and abs(self.pos[1] - s.y) < 20:
                return
            if self.dir == "OESTE" and abs(self.pos[0] - s.x) < 10 and abs(self.pos[1] - s.y) < 20:
                return

        if self.dir == "SUR":
            self.pos[1] += self.vel
        elif self.dir == "NORTE":
            self.pos[1] -= self.vel
        elif self.dir == "ESTE":
            self.pos[0] += self.vel
        elif self.dir == "OESTE":
            self.pos[0] -= self.vel

class GestorSemaforosSur:
    def __init__(self):
        self.semaforos = [
            Semaforo(400, 200, "horizontal"),
            Semaforo(400, 400, "horizontal"),
            Semaforo(300, 300, "vertical"),
            Semaforo(500, 300, "vertical"),
        ]

    def actualizar(self):
        for s in self.semaforos:
            s.actualizar()

    def dibujar(self, ventana):
        for s in self.semaforos:
            s.dibujar(ventana)

class GestorVehiculosSur:
    def __init__(self):
        self.vehiculos = []
        self.cola_vehiculos = queue.Queue()

    def agregar(self, v):
        self.vehiculos.append(v)

    def procesar_cola(self):
        while not self.cola_vehiculos.empty():
            v = self.cola_vehiculos.get()
            self.agregar(v)

    def mover_vehiculos(self, semaforos):
        for v in self.vehiculos:
            v.mover(semaforos)

    async def recibir_callback(self, data):
        try:
            pos, dir_ = generar_spawn_aleatorio()
            v = VehiculoSimulado(
                id_=data.get("id", "???"),
                pos=pos,
                dir_=dir_,
                vel=data.get("velocidad", 0.5) * 10
            )
            print(f"[RECIBIDO] {v.id} -> {v.dir} @ {v.pos}")
            self.cola_vehiculos.put(v)
        except Exception as e:
            print("[ERROR] Al procesar vehículo:", e)

def generar_spawn_aleatorio():
    origen = random.choice(["NORTE", "SUR", "ESTE", "OESTE"])
    if origen == "NORTE":
        return [random.choice([290, 390, 490]), 0], "SUR"
    elif origen == "SUR":
        return [random.choice([290, 390, 490]), ALTO], "NORTE"
    elif origen == "ESTE":
        return [ANCHO, random.choice([190, 290, 390])], "OESTE"
    elif origen == "OESTE":
        return [0, random.choice([190, 290, 390])], "ESTE"

def lanzar_pygame(gestor_vehiculos, gestor_semaforos):
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulación Zona Sur")
    reloj = pygame.time.Clock()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        ventana.fill(COLOR_FONDO)
        # Dibujar calles
        pygame.draw.rect(ventana, COLOR_CALLE, (0, 280, ANCHO, 40))
        pygame.draw.rect(ventana, COLOR_CALLE, (0, 180, ANCHO, 40))
        pygame.draw.rect(ventana, COLOR_CALLE, (0, 380, ANCHO, 40))
        pygame.draw.rect(ventana, COLOR_CALLE, (380, 0, 40, ALTO))
        pygame.draw.rect(ventana, COLOR_CALLE, (280, 0, 40, ALTO))
        pygame.draw.rect(ventana, COLOR_CALLE, (480, 0, 40, ALTO))

        gestor_semaforos.dibujar(ventana)
        gestor_semaforos.actualizar()

        gestor_vehiculos.procesar_cola()
        gestor_vehiculos.mover_vehiculos(gestor_semaforos.semaforos)

        for v in gestor_vehiculos.vehiculos:
            pygame.draw.rect(ventana, COLOR_VEHICULO, (*v.pos, 20, 10))

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

async def main():
    print("[Zona Sur] Esperando vehículos...")
    gestor_vehiculos = GestorVehiculosSur()
    gestor_semaforos = GestorSemaforosSur()

    threading.Thread(target=lanzar_pygame, args=(gestor_vehiculos, gestor_semaforos)).start()
    await recibir_vehiculos("zona_sur", gestor_vehiculos.recibir_callback)

if __name__ == "__main__":
    asyncio.run(main())

