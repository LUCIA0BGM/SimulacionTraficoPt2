import asyncio 
import pygame
import threading
import queue
import random
import uuid    
from comunicacion.mensajeria import recibir_vehiculos, enviar_vehiculo
from zonas.reporte_estado import ReportadorZona
from servicios.vehiculos import VehiculoSimulado, crear_vehiculo_desde_dict
from servicios.semaforos import Semaforo

ANCHO, ALTO = 800, 600
COLOR_FONDO = (30, 30, 30)
COLOR_CALLE = (70, 70, 70)
COLOR_VEHICULO = (0, 200, 255)
COLOR_SEMAFORO = {"rojo": (255, 0, 0), "verde": (0, 255, 0)}

class ZonaSimulada:
    def __init__(self, nombre, cola_entrada, mapa_zonal):
        self.nombre = nombre
        self.cola_entrada = cola_entrada
        self.mapa_zonal = mapa_zonal
        self.cola_vehiculos = queue.Queue()
        self.vehiculos = []
        self.migraciones = asyncio.Queue()

        self.semaforos = [
            Semaforo(400, 200, "horizontal"),
            Semaforo(400, 400, "horizontal"),
            Semaforo(300, 300, "vertical"),
            Semaforo(500, 300, "vertical"),
        ]

        for _ in range(5):
            pos, dir_ = self.generar_spawn_aleatorio()
            
            v = VehiculoSimulado(
                id_=str(uuid.uuid4()),
                pos=pos,
                dir_=dir_,
                vel=3
            )
            self.vehiculos.append(v)

        self.reportador = ReportadorZona(
            nombre_zona=self.nombre,
            obtener_estado_callback=self.estado_actual
        )

    def generar_spawn_aleatorio(self):
        origen = random.choice(["NORTE", "SUR", "ESTE", "OESTE"])
        if origen == "NORTE":
            return [random.choice([290, 390, 490]), 0], "SUR"
        elif origen == "SUR":
            return [random.choice([290, 390, 490]), ALTO], "NORTE"
        elif origen == "ESTE":
            return [ANCHO, random.choice([190, 290, 390])], "OESTE"
        elif origen == "OESTE":
            return [0, random.choice([190, 290, 390])], "ESTE"

    async def recibir_callback(self, data):
        v = crear_vehiculo_desde_dict(data)
        print(f"[{self.nombre}] Recibido {v.id} en {v.pos}")
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
                v.mover(self.semaforos, self)
                pygame.draw.rect(ventana, COLOR_VEHICULO, (*v.pos, 20, 10))

            pygame.display.flip()
            reloj.tick(60)

        pygame.quit()

    async def lanzar(self):
        self.loop_principal = asyncio.get_running_loop()
        print(f"[{self.nombre}] Escuchando en {self.cola_entrada}...")
        self.reportador.iniciar()

        async def generar_vehiculos_periodicamente():
            while True:
                await asyncio.sleep(5)
                pos, dir_ = self.generar_spawn_aleatorio()
                nuevo = VehiculoSimulado(
                    id_=str(uuid.uuid4()),
                    pos=pos,
                    dir_=dir_,
                    vel=3
                )
                print(f"[{self.nombre}] Vehículo nuevo generado: {nuevo.id} -> {dir_} @ {pos}")
                self.cola_vehiculos.put(nuevo)

        async def procesar_migraciones():
            while True:
                vehiculo = await self.migraciones.get()
                destino = self.mapa_zonal.obtener_destino_migracion(vehiculo.pos, vehiculo.dir)
                if destino:
                    await self.migrar(vehiculo, destino)

        await asyncio.gather(
            recibir_vehiculos(self.cola_entrada, self.recibir_callback),
            generar_vehiculos_periodicamente(),
            procesar_migraciones()
        )   

    def estado_actual(self):
        total = len(self.vehiculos)
        congestion = min(1.0, total / 20)
        return total, congestion
