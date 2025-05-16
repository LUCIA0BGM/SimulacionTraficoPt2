# simulacion_trafico/ui/gui.py

import asyncio
import pygame

GRIS_CARRETERA = (80, 80, 80)
AZUL_VEHICULO = (30, 144, 255)
ROJO_SEMAFORO = (255, 0, 0)
VERDE_SEMAFORO = (0, 200, 0)
FONDO = (230, 230, 230)

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 30

TAM_VEHICULO = 10
TAM_SEMAFORO = 10

def transformar_pos(pos):
    x, y = pos
    return int(x * 10 + 50), int(y * 10 + 50)

async def launch_gui(simulator):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Simulador de Tráfico")
    reloj = pygame.time.Clock()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill(FONDO)

        # Calles
        for calle in simulator.city.calles:
            x1, y1 = transformar_pos(calle.inicio)
            x2, y2 = transformar_pos(calle.fin)
            pygame.draw.line(pantalla, GRIS_CARRETERA, (x1, y1), (x2, y2), 20)

        # Vehículos
        for vehiculo in simulator.city.vehicles:
            x, y = transformar_pos(vehiculo.position)
            pygame.draw.rect(pantalla, AZUL_VEHICULO, (x, y, TAM_VEHICULO, TAM_VEHICULO))

        # Semáforos
        for s in simulator.city.traffic_lights:
            x, y = transformar_pos(s.position)
            color = VERDE_SEMAFORO if s.state == "verde" else ROJO_SEMAFORO
            pygame.draw.circle(pantalla, color, (x, y), TAM_SEMAFORO)

        pygame.display.flip()
        reloj.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()