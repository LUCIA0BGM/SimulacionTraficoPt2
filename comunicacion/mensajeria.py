
import aio_pika
import asyncio
import json

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def conectar():
    return await aio_pika.connect_robust(RABBITMQ_URL)

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
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                vehiculo_dict = json.loads(message.body.decode())
                await callback(vehiculo_dict)
