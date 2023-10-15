import json
import logging


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected")
    else:
        logging.error(f"Connection Failure(code={rc})")


def on_disconnect(client, userdata, flags, rc=0):
    logging.info(f"Disconnected(reason={rc})")


def on_publish(client, userdata, mid):
    logging.debug(f"Message[{mid}] was published")


def setup(client):
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect


def period():
    import device.data as data
    return min(300, max(60, data.STATUS_PERIOD * 1000))


def device_packet(register=False):
    import struct
    import device.data as data
    action = 0x00 if register else 0x01
    _type = 0b100001
    s1 = (action << 6) | _type
    s2 = period()
    return struct.pack(">BHI", s1, s2, data.SERIAL)


def report_start(client):
    client.loop_start()
    import time
    import device.data as data
    time.sleep(min(1, max(0.5, data.STATUS_PERIOD * 5)))
    client.publish("device/register", device_packet(True), 1)
    counter = period()
    while True:
        packet = data.packet_data()
        client.publish(f"device/{data.SERIAL}/data", packet, 1)
        _wait = max(0.1, data.STATUS_PERIOD)
        time.sleep(_wait)
        counter -= _wait
        if counter < 0:
            counter = period()
            client.publish("device/ping", device_packet(), 1)
