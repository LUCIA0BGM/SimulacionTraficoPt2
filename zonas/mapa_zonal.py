class MapaZonal:
    """
    Define los límites físicos de la zona y las zonas vecinas según dirección.
    """
    def __init__(self, nombre_zona, limites, vecinos):
        """
        limites: dict con claves 'x_min', 'x_max', 'y_min', 'y_max'
        vecinos: dict con claves ['NORTE', 'SUR', 'ESTE', 'OESTE'] -> nombre de zona vecina
        """
        self.nombre = nombre_zona
        self.limites = limites
        self.vecinos = vecinos

    def obtener_destino_migracion(self, posicion, direccion):
        x, y = posicion
        if direccion == "SUR" and y > self.limites["y_max"]:
            return self.vecinos.get("SUR")
        if direccion == "NORTE" and y < self.limites["y_min"]:
            return self.vecinos.get("NORTE")
        if direccion == "ESTE" and x > self.limites["x_max"]:
            return self.vecinos.get("ESTE")
        if direccion == "OESTE" and x < self.limites["x_min"]:
            return self.vecinos.get("OESTE")
        return None
