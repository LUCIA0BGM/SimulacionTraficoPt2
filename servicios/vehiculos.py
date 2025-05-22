import uuid
import random

class VehiculoSimulado:
    def __init__(self, id_, pos, dir_, vel):
        self.id = id_
        self.pos = list(pos)
        self.dir = dir_
        self.vel = vel
        self.migrando = False

    def mover(self, semaforos, zona_actual):
        if self.migrando:
            return

        for s in semaforos:
            if not s.permite_pasar(self):
                if self._cerca_de(s):
                    return

        self._avanzar()

        destino = zona_actual.mapa_zonal.obtener_destino_migracion(self.pos, self.dir)
        if destino:
            print(f"[DEBUG] {self.id} detectado para migración hacia {destino} desde pos {self.pos}")
            self.migrando = True
            zona_actual.loop_principal.call_soon_threadsafe(
                zona_actual.migraciones.put_nowait, self
            )

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


def crear_vehiculo_desde_dict(data, zona):
    pos = data.get("posicion", [400, 0])
    dir_ = data.get("direccion", "SUR")
    vel = data.get("velocidad", 0.5) * 10

    # 🔁 Corrige la posición si entra desde otra zona
    if dir_ == "SUR":
        pos[1] = 0  # entra por el norte
    elif dir_ == "NORTE":
        pos[1] = 580  # entra por el sur
    elif dir_ == "ESTE":
        pos[0] = 0  # entra por el oeste
    elif dir_ == "OESTE":
        pos[0] = 780  # entra por el este

    return VehiculoSimulado(
        id_=data.get("id", "???"),
        pos=pos,
        dir_=dir_,
        vel=vel
    )
