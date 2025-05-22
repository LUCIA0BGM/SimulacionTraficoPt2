# interfaz/gui.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard de Tráfico Distribuido</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 20px; }
        h1 { color: #333; }
        .zona { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
        .congestion { font-weight: bold; }
    </style>
</head>
<body>
    <h1>Estado Actual de la Simulación</h1>
    <div id="zonas">Cargando estado...</div>

    <script>
        async function cargarEstado() {
            try {
                const response = await fetch("http://localhost:8000/estado");
                const data = await response.json();
                const contenedor = document.getElementById("zonas");
                contenedor.innerHTML = "";

                for (const zona in data) {
                    const div = document.createElement("div");
                    div.className = "zona";
                    div.innerHTML = `
                        <h3>${zona}</h3>
                        <p>Vehículos: ${data[zona].vehiculos}</p>
                        <p class="congestion">Congestión: ${(data[zona].congestion * 100).toFixed(0)}%</p>
                    `;
                    contenedor.appendChild(div);
                }
            } catch (error) {
                document.getElementById("zonas").innerText = "Error al cargar estado.";
            }
        }

        cargarEstado();
        setInterval(cargarEstado, 2000);  // refresca cada 2 segundos
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def root():
    return html_template
