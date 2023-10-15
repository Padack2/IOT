import paho.mqtt.client as mqtt
import struct

client = mqtt.Client()

active = 1
period = 10
target = 18
message = struct.pack(">BBh", (active << 7) | period, 0, target)

client.connect("localhost", 1883)
client.loop_start()
client.publish("device/1/control", message, 1)
client.subscribe("device/ping", 1)
client.subscribe("device/register", 1)
client.loop_stop()
client.disconnect()
