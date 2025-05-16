# simulacion_trafico/concurrency/tasks.py

import asyncio

async def mover_vehiculo(v, city, intervalo=0.5):
    while True:
        v.mover(city)
        await asyncio.sleep(intervalo)

async def cambiar_semaforo(s, intervalo=5):
    while True:
        s.cambiar_estado()
        await asyncio.sleep(intervalo)

def run_simulation_tasks(simulator, update_interval=0.5):
    tasks = []
    for v in simulator.city.vehicles:
        tasks.append(asyncio.create_task(mover_vehiculo(v, simulator.city, update_interval)))
    for s in simulator.city.traffic_lights:
        tasks.append(asyncio.create_task(cambiar_semaforo(s)))
    return tasks
