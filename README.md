
# Documentación Técnica - Simulación de Tráfico Distribuida

## 1. Resumen del Proyecto

Este proyecto consiste en una simulación distribuida de tráfico urbano en tiempo real, desarrollada en Python. Se ha dividido la ciudad en zonas, cada una ejecutada como un nodo independiente, con microservicios responsables de la gestión de vehículos, semáforos, coordinación, salud y comunicación. La simulación visual se realiza con `Pygame`, y la comunicación entre nodos se lleva a cabo mediante `RabbitMQ`.

---

## 2. Arquitectura General del Sistema

La estructura del proyecto sigue una arquitectura modular basada en microservicios:

```
simulacion_distribuida/
├── main.py
├── servicios/
│   ├── vehiculos.py
│   ├── semaforos.py
│   ├── reporte_estado.py
│   ├── coordinador.py
│   └── salud.py
├── comunicacion/
│   └── mensajeria.py
├── concurrency/
│   └── tasks.py
├── interfaz/
│   └── gui.py
├── distribuition/
│   └── rabbit_client.py
├── docker/
│   └── Dockerfile
├── simulation/
│   └── simulator.py
├── utils.py
└── zonas/
    ├── zona_norte.py
    ├── zona_sur.py
    ├── mapa_zonal.py
    └── simulador_zona.py
```

Cada zona lanza su propia instancia Pygame, escucha su cola RabbitMQ y reporta su estado al coordinador.

---

## 3. Microservicios y Responsabilidades

- **vehiculos.py**: lógica de movimiento, migración y creación de vehículos.
- **semaforos.py**: comportamiento, dibujo y lógica de semáforos.
- **coordinador.py**: recepción de reportes, monitoreo del estado global, API con FastAPI.
- **salud.py**: endpoint `/health` para verificar que el coordinador esté activo.
- **rabbitmq_client.py**: envío y recepción de mensajes entre zonas.
- **gui.py**: muestra en tiempo real la congestión de cada zona.
- **utils.py**: funciones comunes (generación aleatoria, constantes de dirección).

---

## 4. Migración y Sincronización de Vehículos

Los vehículos se detectan automáticamente en los bordes de cada zona. Al llegar al borde:

1. Se encolan para migrar.
2. Se envía su estado al nodo destino mediante RabbitMQ.
3. El nodo destino los integra en su simulación, manteniendo carril y dirección.

---

## 5. Coordinación y Balanceo de Carga

- El **coordinador** expone un endpoint `/reportar` donde las zonas reportan su estado (`vehiculos`, `congestion`).
- El dashboard visual (`gui.py`) muestra en tiempo real el estado de cada zona.
- La lógica de balanceo dinámico está preparada para extenderse a un algoritmo de redistribución.

---

## 6. Optimización y Tolerancia a Fallos

- Cada nodo es autónomo y puede reiniciarse sin afectar a los demás.
- El coordinador expone `/health` para monitoreo.
- RabbitMQ garantiza entrega de mensajes asíncronos.
- Uso de `asyncio` en todos los hilos de comunicación y migración.

---

## 7. Interfaz Gráfica y Monitoreo

- Cada zona se muestra con Pygame, incluyendo:
  - Vehículos en movimiento.
  - Semáforos dinámicos.
- El coordinador puede mostrar gráficamente el estado de cada zona (`gui.py`).
- Cada nodo imprime eventos clave por consola.

---

## 8. Pruebas Realizadas

- Migración fluida de vehículos entre zonas.
- Generación periódica de vehículos en entradas permitidas.
- Trazado de congestión por zona.
- Tolerancia al reinicio de zonas o coordinador.
- Consumo y procesamiento correcto de colas RabbitMQ.

---

## 9. Despliegue y Ejecución

1. Instalar dependencias: `pip install -r requirements.txt`
2. Iniciar RabbitMQ (`docker-compose` o manual).
3. Lanzar coordinador: `python -m servicios.coordinador`
4. Lanzar zona norte y sur:
   ```bash
   python -m zonas.zona_norte
   python -m zonas.zona_sur
   ```
5. (Opcional) Ejecutar GUI central:
   ```bash
   python -m interfaz.gui
   ```

---

## 10. Conclusiones y Mejoras Futuras

- El sistema es modular, distribuido y tolerante a fallos básicos.
- Podría mejorarse:
  - Agregando lógica de balanceo basada en congestión.
  - Persistencia de estado tras reinicios.
  - Dashboard web con Flask/FastAPI.
  - Monitoreo Prometheus/Grafana.
  - Uso de Docker para contenerización completa.

