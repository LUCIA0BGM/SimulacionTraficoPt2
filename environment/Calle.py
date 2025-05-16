
class Calle:
    def __init__(self, nombre, inicio, fin, direccion):
        self.nombre = nombre
        self.inicio = inicio  # (x, y)
        self.fin = fin        # (x, y)
        self.direccion = direccion  # "horizontal" o "vertical"
        self.vehiculos = []

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def remover_vehiculo(self, vehiculo):
        if vehiculo in self.vehiculos:
            self.vehiculos.remove(vehiculo)
