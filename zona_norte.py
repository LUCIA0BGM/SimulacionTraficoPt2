
import asyncio
import random
from comunicacion.mensajeria import enviar_vehiculo

async def generar_vehiculos():
    while True:
        vehiculo = {
            "id": f"veh_{random.randint(1000, 9999)}",
            "posicion": [random.uniform(0, 10), 49.5],
            "direccion": "SUR",
            "velocidad": round(random.uniform(0.3, 0.6), 2)
        }
        print(f"[Zona Norte] Enviando vehículo: {vehiculo['id']}")
        await enviar_vehiculo(vehiculo, "zona_sur")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(generar_vehiculos())
