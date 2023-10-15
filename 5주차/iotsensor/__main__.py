import paho.mqtt.client as mqtt
from iotsensor import publish as pub

client = mqtt.Client()

client.on_connect = pub.on_connect
client.on_disconnect = pub.on_disconnect
client.on_publish = pub.on_publish

from iotsensor import sensor

client.connect("localhost", 1883)
sensor.start(client)
client.disconnect()