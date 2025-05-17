# servicios/coordinador.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uvicorn

app = FastAPI(title="Coordinador Central de Tráfico")

# Estado actual reportado por cada zona
estado_zonas: Dict[str, dict] = {}

class EstadoZona(BaseModel):
    zona: str
    vehiculos: int
    congestion: float  # porcentaje entre 0.0 y 1.0
    timestamp: float

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

if __name__ == "__main__":
    uvicorn.run("coordinador:app", host="0.0.0.0", port=8000, reload=True)
