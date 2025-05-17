import asyncio
import pygame
import threading
import queue
import random
from comunicacion.mensajeria import recibir_vehiculos, enviar_vehiculo

ANCHO, ALTO = 800, 600
COLOR_FONDO = (30, 30, 30)
COLOR_CALLE = (70, 70, 70)
COLOR_VEHICULO = (0, 200, 255)
COLOR_SEMAFORO = {"rojo": (255, 0, 0), "verde": (0, 255, 0)}

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

    def mover(self, semaforos, zona_actual, zona_destino):
        for s in semaforos:
            if not s.permite_pasar(self):
                if self._cerca_de(s):
                    return

        self._avanzar()

        # Migrar si sale del borde inferior
        if self.pos[1] > ALTO and self.dir == "SUR":
            asyncio.create_task(zona_actual.migrar(self, zona_destino))

    def _avanzar(self):
        if self.dir == "SUR":
            self.pos[1] += self.vel
        elif self.dir == "NORTE":
            self.pos[1] -= self.vel
        elif self.dir == "ESTE":
            self.pos[0] += self.vel
        elif self.dir == "OESTE":
            self.pos[0] -= self.vel

    def _cerca_de(self, semaforo):
        return (
            (self.dir == "SUR" and abs(self.pos[1] - semaforo.y) < 10 and abs(self.pos[0] - semaforo.x) < 20) or
            (self.dir == "NORTE" and abs(self.pos[1] - semaforo.y) < 10 and abs(self.pos[0] - semaforo.x) < 20) or
            (self.dir == "ESTE" and abs(self.pos[0] - semaforo.x) < 10 and abs(self.pos[1] - semaforo.y) < 20) or
            (self.dir == "OESTE" and abs(self.pos[0] - semaforo.x) < 10 and abs(self.pos[1] - semaforo.y) < 20)
        )

class ZonaSimulada:
    def __init__(self, nombre, cola_entrada, zona_destino):
        self.nombre = nombre
        self.cola_entrada = cola_entrada
        self.zona_destino = zona_destino
        self.cola_vehiculos = queue.Queue()
        self.vehiculos = []
        self.semaforos = [
            Semaforo(400, 200, "horizontal"),
            Semaforo(400, 400, "horizontal"),
            Semaforo(300, 300, "vertical"),
            Semaforo(500, 300, "vertical"),
        ]

    async def recibir_callback(self, data):
        pos = [random.randint(300, 500), 0]
        v = VehiculoSimulado(
            id_=data.get("id", "???"),
            pos=pos,
            dir_="SUR",
            vel=data.get("velocidad", 0.5) * 10
        )
        print(f"[{self.nombre}] Recibido {v.id}")
        self.cola_vehiculos.put(v)

    async def migrar(self, vehiculo, destino):
        print(f"[{self.nombre}] Migrando {vehiculo.id} -> {destino}")
        await enviar_vehiculo({
            "id": vehiculo.id,
            "posicion": vehiculo.pos,
            "direccion": vehiculo.dir,
            "velocidad": vehiculo.vel / 10
        }, destino)
        self.vehiculos = [v for v in self.vehiculos if v.id != vehiculo.id]

    def lanzar_pygame(self):
        pygame.init()
        ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(f"Simulación: {self.nombre}")
        reloj = pygame.time.Clock()

        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            ventana.fill(COLOR_FONDO)
            pygame.draw.rect(ventana, COLOR_CALLE, (0, 280, ANCHO, 40))
            pygame.draw.rect(ventana, COLOR_CALLE, (0, 180, ANCHO, 40))
            pygame.draw.rect(ventana, COLOR_CALLE, (0, 380, ANCHO, 40))
            pygame.draw.rect(ventana, COLOR_CALLE, (380, 0, 40, ALTO))
            pygame.draw.rect(ventana, COLOR_CALLE, (280, 0, 40, ALTO))
            pygame.draw.rect(ventana, COLOR_CALLE, (480, 0, 40, ALTO))

            for s in self.semaforos:
                s.actualizar()
                s.dibujar(ventana)

            while not self.cola_vehiculos.empty():
                v = self.cola_vehiculos.get()
                self.vehiculos.append(v)

            for v in self.vehiculos:
                v.mover(self.semaforos, self, self.zona_destino)
                pygame.draw.rect(ventana, COLOR_VEHICULO, (*v.pos, 20, 10))

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    async def lanzar(self):
        print(f"[{self.nombre}] Escuchando en {self.cola_entrada}...")
        await recibir_vehiculos(self.cola_entrada, self.recibir_callback)
