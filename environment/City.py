# simulacion_trafico/environment/city.py

from environment.Calle import Calle
from environment.Interseccion import Interseccion

class City:
    def __init__(self, name):
        self.name = name
        self.calles = []
        self.intersecciones = []
        self.vehicles = []
        self.traffic_lights = []

    def add_calle(self, calle):
        self.calles.append(calle)

    def add_interseccion(self, interseccion):
        self.intersecciones.append(interseccion)

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)
