from aiokafka import AIOKafkaProducer
from buildhat import ColorSensor
import asyncio

async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers='kafka.prometheus.io:9092')
    color = ColorSensor('C')

    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        while True:
            c = color.wait_for_new_color()

            # Produce message
            await producer.send_and_wait("network", bytes(c, encoding='utf-8'))
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

asyncio.run(send_one())
