import random
import struct

import device.data as data

TOPIC = f"device/{data.SERIAL}/control"


def on_message(client, userdata, message):
    if message.topic == TOPIC:
        on_control(message.payload)


import logging


def on_control(packet):
    import device.data as data
    s1, r1, value = struct.unpack(">BBh", packet)
    active = (s1 >> 7) & 0x1
    period = (s1 & 0x7f) / 10.0
    logging.info(f"CONTROL[active={active}, period={period}sec, target-value={value}")
    if active:
        data.set_active()
    else:
        data.set_idle()
    data.STATUS_PERIOD = period
    data.change_target(value)


import time


def start(client):
    client.on_message = on_message
    client.subscribe(TOPIC, 1)
    while True:
        time.sleep(0.2)
        if not data.STATUS_CONTROL:
            continue
        if data.TARGET > data.CURRENT:
            data.CURRENT += 0.01
        elif data.TARGET < data.CURRENT:
            data.CURRENT -= 0.01
        else:
            data.STATUS_CONTROL = 0
