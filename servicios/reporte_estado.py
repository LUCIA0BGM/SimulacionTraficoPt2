# servicios/estado.py

import time
import asyncio
import httpx

class ReportadorZona:
    def __init__(self, nombre_zona, obtener_estado_callback, intervalo=5, url_coordinador="http://localhost:8000/estado"):
        self.nombre_zona = nombre_zona
        self.obtener_estado = obtener_estado_callback  # debe devolver (vehiculos: int, congestion: float)
        self.intervalo = intervalo
        self.url = url_coordinador
        self._detener = False

    async def _reportar_estado(self):
        async with httpx.AsyncClient() as client:
            while not self._detener:
                vehiculos, congestion = self.obtener_estado()
                estado = {
                    "zona": self.nombre_zona,
                    "vehiculos": vehiculos,
                    "congestion": congestion,
                    "timestamp": time.time()
                }
                try:
                    resp = await client.post(self.url, json=estado)
                    print(f"[Reporte] Enviado estado de {self.nombre_zona}: {resp.status_code}")
                except Exception as e:
                    print(f"[Reporte] Error al reportar: {e}")
                await asyncio.sleep(self.intervalo)

    def iniciar(self):
        asyncio.create_task(self._reportar_estado())

    def detener(self):
        self._detener = True
