# servicios/coordinador.py

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict
import uvicorn
from fastapi.responses import JSONResponse


app = FastAPI(title="Coordinador Central de Tráfico")

# Estado actual reportado por cada zona
estado_zonas = {}

class EstadoZona(BaseModel):
    zona: str
    vehiculos: int
    congestion: float  # porcentaje entre 0.0 y 1.0
    timestamp: float

@app.post("/reportar")
async def reportar_estado(request: Request):
    datos = await request.json()
    zona = datos.get("zona")
    vehiculos = datos.get("vehiculos", 0)
    congestion = datos.get("congestion", 0.0)

    if zona:
        estado_zonas[zona] = {"vehiculos": vehiculos, "congestion": congestion}
        print(f"[Coordinador] Estado actualizado para {zona}: {estado_zonas[zona]}")
        return {"mensaje": "Estado recibido"}
    else:
        return JSONResponse(status_code=400, content={"error": "Zona no especificada"})

@app.post("/estado")
async def recibir_estado_zona(estado: EstadoZona):
    estado_zonas[estado.zona] = {
        "vehiculos": estado.vehiculos,
        "congestion": estado.congestion,
        "timestamp": estado.timestamp
    }
    return {"mensaje": f"Estado recibido de {estado.zona}"}

@app.get("/zonas")
async def obtener_estados():
    return estado_zonas

@app.get("/zonas/{nombre}")
async def obtener_estado_zona(nombre: str):
    if nombre not in estado_zonas:
        raise HTTPException(status_code=404, detail="Zona no registrada")
    return estado_zonas[nombre]

@app.get("/health")
async def health_check():
    return {"estado": "ok", "descripcion": "El servicio coordinador está activo."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

