import struct
from collections import namedtuple

CHANNEL_DEVICE_REGISTER = "device/register"
CHANNEL_DEVICE_PING = "device/ping"
CHANNEL_DEVICE_DATA = "device/{DEVICE}/data"
CHANNEL_DEVICE_CONTROL = "device/{DEVICE}/control"

DevicePing = namedtuple("DevicePing", "action type period serial", rename=True)
DeviceData = namedtuple("DeviceData", "serial payload")


def decode_ping(payload: bytes) -> DevicePing:
    first_byte = payload[0]
    action = (first_byte >> 6) & 0x3  # 0x3 = 0b11 (2bit)
    _type = first_byte & 0x3f  # 0x3f = 0b111111    (6bit)
    second = payload[1:]
    period, serial = struct.unpack(">HI", second)
    return DevicePing(action=action, type=_type, period=period, serial=serial)


def decode_data(payload: bytes) -> DeviceData:
    first = payload[:4]
    serial, = struct.unpack(">I", first)
    data_payload = payload[4:]
    return DeviceData(serial, data_payload)
