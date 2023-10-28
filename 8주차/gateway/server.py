import re
import time
from datetime import datetime

import paho.mqtt.client

from gateway import protocol


def on_message(client, userdata, message):
    if message.topic == protocol.CHANNEL_DEVICE_REGISTER:
        on_register(client, message)  # on_register(client, message)
    elif message.topic == protocol.CHANNEL_DEVICE_PING:
        on_passive_ping(message)
    else:
        pattern = protocol.CHANNEL_DEVICE_DATA.format(DEVICE="(.*)")
        regex = re.compile(pattern)
        matched = regex.match(message.topic)
        if matched:
            serial = matched.group(1)
            on_received_data(client, serial, message)


def on_received_data(client, serial, message):
    logging.info(f"[RECEIVED] {message.topic}")
    if not devices.is_exists(serial):
        logging.warning(f"[NO DEV] {message.topic} is not matched")
        client.unsubscribe(message.topic)
        return
    data = protocol.decode_data(message.payload)
    dev = devices.DEVICES[data.serial]  # type: devices.DeviceMeta
    logging.info(f"SERIAL = {dev.serial}, TYPE = {dev.type:b}")
    dev.extra["raw"] = data.payload
    if dev.type == 0b100001:
        from gateway.sensors import virtual
        reported = virtual.decode_payload(data.payload)
        dev.extra["reported"] = reported
        logging.info(f"[VIRTUAL TEMP:{dev.type:b}] status = {reported.status} "
                     f"battery = {reported.battery} "
                     f"controlled = {reported.controlled} "
                     f"metric period = {reported.metric_period} \n\t\t"
                     f"target value = {reported.change_target} "
                     f"current value = {reported.current}")


from gateway import devices

import logging


def on_register(client, message):
# def on_register(message):
    logging.info(f"[REGISTER] {message.topic}")
    reg = protocol.decode_ping(message.payload)
    logging.info(f"SERIAL = {reg.serial}, TYPE = {reg.type}, PERIOD = {reg.period}")
    devices.register(reg.serial, reg.type, reg.period)
    client.subscribe(protocol.CHANNEL_DEVICE_DATA.format(DEVICE=reg.serial))


def on_passive_ping(message):
    logging.info(f"[PASSIVE PING] {message.topic}")
    reg = protocol.decode_ping(message.payload)
    logging.info(f"SERIAL = {reg.serial}, TYPE = {reg.type}, PERIOD = {reg.period}")
    devices.set_alive(reg.serial, reg.period)


import paho.mqtt.client


def start(client: paho.mqtt.client.Client):
    client.on_message = on_message
    client.subscribe(protocol.CHANNEL_DEVICE_REGISTER, qos=1)
    client.subscribe(protocol.CHANNEL_DEVICE_PING, qos=1)
    client.loop_forever()


def manager():
    while True:
        _next = None  # type: devices.DeviceMeta
        for s, dev in devices.DEVICES.items():  # type: devices.DeviceMeta
            if not _next:
                _next = dev
            elif _next.next > dev.next:
                _next = dev

        if _next:
            now = datetime.now()
            logging.info(f"[NEXT] {dev.serial} : {_next.next}")
            time.sleep((_next.next - now).total_seconds())
            if devices.DEVICES[_next.serial] == _next:
                devices.miss_ping(_next.serial)
        else:
            time.sleep(5)


def run_manager_thread():
    import threading

    t = threading.Thread(
        target=manager, daemon=True)
    t.start()
    return t


def run_message_thread(client):
    import threading

    t = threading.Thread(
        target=start, daemon=True,
        args=(client,))
    t.start()
    return t


def create_client():
    import paho.mqtt.client as mqtt
    client = mqtt.Client()
    client.connect("localhost", 1883)
    return client
