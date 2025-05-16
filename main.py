# simulacion_trafico/main.py

import asyncio

from environment.City import City
from environment.Calle import Calle
from environment.Interseccion import Interseccion
from environment.Vehicle import Vehicle
from environment.TrafficLight import TrafficLight
from simulation.simulator import Simulator
from concurrency.tasks import run_simulation_tasks
from ui.gui import launch_gui


async def main():
    city = City(name="Ciudad Inteligente")

    # Crear calles
    calle1 = Calle("Calle Norte", (0, 5), (50, 5), "horizontal")
    calle2 = Calle("Calle Sur", (0, 10), (50, 10), "horizontal")
    calle3 = Calle("Calle Este", (10, 0), (10, 50), "vertical")
    calle4 = Calle("Calle Oeste", (20, 0), (20, 50), "vertical")

    city.add_calle(calle1)
    city.add_calle(calle2)
    city.add_calle(calle3)
    city.add_calle(calle4)

    # Crear intersecciones con semáforos
    inter1 = Interseccion((10, 5))
    inter2 = Interseccion((20, 5))
    inter3 = Interseccion((10, 10))
    inter4 = Interseccion((20, 10))

    sem1 = TrafficLight("S1", 4, 1, 3, position=(10, 5))
    sem2 = TrafficLight("S2", 4, 1, 3, position=(20, 5))
    sem3 = TrafficLight("S3", 4, 1, 3, position=(10, 10))
    sem4 = TrafficLight("S4", 4, 1, 3, position=(20, 10))

    inter1.asignar_semaforo(sem1)
    inter2.asignar_semaforo(sem2)
    inter3.asignar_semaforo(sem3)
    inter4.asignar_semaforo(sem4)

    city.add_interseccion(inter1)
    city.add_interseccion(inter2)
    city.add_interseccion(inter3)
    city.add_interseccion(inter4)

    city.add_traffic_light(sem1)
    city.add_traffic_light(sem2)
    city.add_traffic_light(sem3)
    city.add_traffic_light(sem4)

    # Crear vehículos sobre calles
    v1 = Vehicle("V1", position=[0, 5], speed=0.5, direction="ESTE")
    v2 = Vehicle("V2", position=[0, 10], speed=0.3, direction="ESTE")
    v3 = Vehicle("V3", position=[10, 0], speed=0.4, direction="SUR")

    city.add_vehicle(v1)
    city.add_vehicle(v2)
    city.add_vehicle(v3)

    simulator = Simulator(city)
    tasks = run_simulation_tasks(simulator, update_interval=0.2)
    gui_task = asyncio.create_task(launch_gui(simulator))
    await asyncio.gather(*tasks, gui_task)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())