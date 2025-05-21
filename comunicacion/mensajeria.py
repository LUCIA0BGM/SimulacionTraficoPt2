import aio_pika
import asyncio
import json

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def conectar():
    conn = await aio_pika.connect_robust(RABBITMQ_URL)
    print("[RabbitMQ] Conectado")
    return conn

async def enviar_vehiculo(vehiculo_dict, destino):
    connection = await conectar()
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(vehiculo_dict).encode()),
            routing_key=destino,
        )

async def recibir_vehiculos(queue_name, callback):
    connection = await conectar()
    channel = await connection.channel()

    queue = await channel.declare_queue(
        name=queue_name,
        durable=True,
        auto_delete=False,
        exclusive=False  # 🔍 asegúrate de que la cree si no existe
    )
    print(f"[RabbitMQ] Cola declarada: {queue.name}")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                body = message.body.decode().strip()
                if not body:
                    print("[RabbitMQ] Mensaje vacío ignorado.")
                    continue

                try:
                    contenido = json.loads(body)
                except json.JSONDecodeError:
                    print(f"[RabbitMQ] JSON inválido: {body}")
                    continue

                if "id" not in contenido:
                    print(f"[RabbitMQ] Mensaje sin ID ignorado: {contenido}")
                    continue

                await callback(contenido)
