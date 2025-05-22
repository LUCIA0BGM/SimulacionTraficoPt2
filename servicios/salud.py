# servicios/salud.py

from fastapi import FastAPI
from prometheus_client import start_http_server, Summary
import threading

# Prometheus metric: tiempo de procesamiento de solicitudes
SOLICITUD_TIEMPO = Summary("solicitud_procesamiento_segundos", "Tiempo en procesar cada solicitud")

app = FastAPI()

@app.get("/health")
@SOLICITUD_TIEMPO.time()
async def health_check():
    return {"estado": "ok", "descripcion": "El servicio está activo."}


def lanzar_servicio_salud(puerto=8001):
    """
    Inicia el servidor FastAPI en un hilo separado para health check.
    """
    import uvicorn

    def iniciar():
        uvicorn.run(app, host="0.0.0.0", port=puerto)

    thread = threading.Thread(target=iniciar, daemon=True)
    thread.start()

    # Inicia servidor Prometheus para exponer métricas en otro puerto
    start_http_server(puerto + 1)
    print(f"[Salud] Health check activo en http://localhost:{puerto}/health")
    print(f"[Salud] Métricas Prometheus en http://localhost:{puerto + 1}")
