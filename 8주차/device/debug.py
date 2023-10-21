import struct

import paho.mqtt.client as mqtt

client = mqtt.Client()


def on_message(client, userdata, message):
    payload = message.payload
    print(f"Topic[{message.topic}]: Payload={payload}")
    # serial, s1, s2, s3, s4, T, C = struct.unpack(">IBBBBhh", payload)
    # active = (s1 >> 7) & 0x1
    # battery = s1 & 0x7f
    # control = (s2 >> 7) & 0x1
    # period = s2 & 0x7f
    #
    # print(f"""Topic[{message.topic}]: SERIAL={serial}, BATTERY={battery}%,
    #                         ACTIVE={active}, CONTROL={control},
    #                         TARGET={T / 100}, CURRENT={C / 100}""")


client.connect("localhost", 1883)
client.on_message = on_message
client.subscribe("device/1/data", 1)
client.subscribe("device/ping", 1)
client.subscribe("device/register", 1)
client.loop_forever()
