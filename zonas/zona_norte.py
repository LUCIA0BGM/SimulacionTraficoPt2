import asyncio
import threading
from zonas.simulador_zona import ZonaSimulada
from zonas.mapa_zonal import MapaZonal

if __name__ == "__main__":
    mapa_norte = MapaZonal(
        nombre_zona="zona_norte",
        limites={"x_min": 0, "x_max": 800, "y_min": 0, "y_max": 300},
        vecinos={"SUR": "zona_sur"}  # puedes añadir más si expandes
    )

    zona_norte = ZonaSimulada("Zona Norte", "zona_norte", mapa_norte)
    threading.Thread(target=zona_norte.lanzar_pygame).start()
    asyncio.run(zona_norte.lanzar())
