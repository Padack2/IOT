import paho.mqtt.client as mqtt
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

from device.run import start

client = mqtt.Client()
client.connect("localhost", 1883)
start(client)
client.disconnect()
