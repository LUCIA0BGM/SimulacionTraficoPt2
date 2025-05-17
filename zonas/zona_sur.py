import asyncio
import threading
from zonas.simulador_zona import ZonaSimulada
from zonas.mapa_zonal import MapaZonal

if __name__ == "__main__":
    mapa_sur = MapaZonal(
        nombre_zona="zona_sur",
        limites={"x_min": 0, "x_max": 800, "y_min": 300, "y_max": 600},
        vecinos={"NORTE": "zona_norte"}  # puedes añadir más si expandes
    )

    zona_sur = ZonaSimulada("Zona Sur", "zona_sur", mapa_sur)
    threading.Thread(target=zona_sur.lanzar_pygame).start()
    asyncio.run(zona_sur.lanzar())
