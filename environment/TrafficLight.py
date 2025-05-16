# simulacion_trafico/environment/traffic_light.py

class TrafficLight:
    """
    Clase que modela un semáforo con tiempos específicos para cada estado.
    """
    def __init__(self, id_, green_time, yellow_time, red_time, position=(5, 5)):
        self.id = id_
        self.green_time = green_time
        self.yellow_time = yellow_time
        self.red_time = red_time
        self.state = "rojo"
        self.time_counter = 0
        self.position = position

    def cambiar_estado(self):
        if self.state == "rojo":
            self.state = "verde"
        elif self.state == "verde":
            self.state = "amarillo"
        elif self.state == "amarillo":
            self.state = "rojo"
        self.time_counter = 0
