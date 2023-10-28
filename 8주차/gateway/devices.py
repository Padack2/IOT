from collections import namedtuple

import gateway.protocol

DEVICES = dict()

DeviceMeta = namedtuple("DeviceMeta", "serial type next period status extra", rename=True)


def register(serial, _type, period):
    from datetime import datetime, timedelta
    DEVICES[serial] = DeviceMeta(
        serial=serial,
        type=_type,
        next=datetime.now() + timedelta(seconds=period),
        period=period,
        status="ALIVE",
        extra=dict()
    )


def set_alive(serial, period=None):
    from datetime import datetime, timedelta
    if serial not in DEVICES:
        raise ValueError(f"{serial} 장치가 없습니다.")
    meta = DEVICES[serial]  # type: DeviceMeta
    if not period:
        period = meta.period
    status = "ALIVE"
    _next = datetime.now() + timedelta(seconds=period)
    DEVICES[serial] = DeviceMeta(serial, meta.type, _next, period, status, meta.extra)


def miss_ping(serial):
    from datetime import datetime, timedelta
    if serial not in DEVICES:
        raise ValueError(f"{serial} 장치가 없습니다.")
    meta = DEVICES[serial]
    status = meta.status
    if meta.status == "ALIVE":
        status = "HANG"
    elif meta.status == "HANG":
        status = "DEAD"
        meta.extra["TIMES"] = 0
    elif meta.status == "DEAD":
        meta.extra["TIMES"] += 1
        if meta.extra["TIMES"] >= 60:
            del DEVICES[serial]
            return
    _next = datetime.now() + timedelta(seconds=meta.period)
    DEVICES[serial] = DeviceMeta(serial, meta.type, _next, meta.period, status, meta.extra)


def is_exists(serial):
    return int(serial) in DEVICES


def is_alive(serial):
    if not is_exists(serial):
        return False
    meta = DEVICES[serial]
    return meta.status == "ALIVE"


def is_hang(serial):
    if not is_exists(serial):
        return False
    meta = DEVICES[serial]
    return meta.status == "HANG"


def is_dead(serial):
    if not is_exists(serial):
        return False
    meta = DEVICES[serial]
    return meta.status == "DEAD"
