import asyncio
import threading
from zonas.simulador_zona import ZonaSimulada
from zonas.mapa_zonal import MapaZonal
import uuid

if __name__ == "__main__":
    mapa_norte = MapaZonal(
        nombre_zona="zona_norte",
        limites={"x_min": 0, "x_max": 800, "y_min": 0, "y_max": 590},
        vecinos={"SUR": "zona_sur"}  # puedes añadir más si expandes
    )

    zona_norte = ZonaSimulada("Zona Norte", "zona_norte", mapa_norte)
    threading.Thread(target=zona_norte.lanzar_pygame).start()
    
    from zonas.simulador_zona import VehiculoSimulado

    # Crear un vehículo en la parte baja de la zona para que migre rápidamente
    vehiculo_prueba = VehiculoSimulado(
        id_=str(uuid.uuid4()),
        pos=[400, 595],  # Posición vertical muy cerca del límite
        dir_="SUR",
        vel=10
    )

    zona_norte.vehiculos.append(vehiculo_prueba)
    print(f"[Zona Norte] Vehículo de prueba añadido: {vehiculo_prueba.id}")

    asyncio.run(zona_norte.lanzar())
