import paho.mqtt.client as mqtt
from iotservice import subscribe as sub

client = mqtt.Client()

client.on_connect = sub.on_connect
client.on_disconnect = sub.on_disconnect
client.on_publish = sub.on_publish

from iotservice import processor

client.connect(
    "localhost",
    1883
)

processor.start(client)