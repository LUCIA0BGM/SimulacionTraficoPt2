import asyncio
import threading
from zonas.simulador_zona import ZonaSimulada

if __name__ == "__main__":
    zona = ZonaSimulada("Zona Sur", "zona_sur", "zona_norte")
    threading.Thread(target=zona.lanzar_pygame).start()
    asyncio.run(zona.lanzar())
