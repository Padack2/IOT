import struct
from collections import namedtuple

VirtualTempDev = namedtuple("VirtualTempDev",
                            "status battery controlled metric_period change_target current")


def decode_payload(payload: bytes):
    s1, s2, s34, change, current = struct.unpack(">BBHHH", payload)
    status = (s1 >> 7) & 0x1
    battery = s1 & 0x7f
    controlled = (s2 >> 7) & 0x1
    metric_period = s2 & 0x7f
    return VirtualTempDev(
        status, battery, controlled, metric_period, change, current
    )
