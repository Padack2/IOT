"""장치의 데이터 관리"""
import struct

SERIAL = 0x1
"""장치 시리얼, 32bit """
STATUS = 0x0
"""장치 상태, 32bit"""
STATUS_RUN = 0
"""장치 상태 중, 동작 비트(1bit): 0:Idle, 1:Run"""
STATUS_BATTERY = 100
"""장치 상태 중, 배터리 잔량: 0~100 (7bit)"""
STATUS_CONTROL = 0
"""장치 상태 중, 목표 온도 변경: 0: Stay, 1: Set"""
STATUS_PERIOD = 1.0  # Seconds
"""장치 상태 중, 목표 온도 측정 주기: 1/10 seconds"""
TARGET = 0.0
"""장치 목표 온도, 16bit"""
CURRENT = 0.0
"""장치 현재 온도, 16bit"""


def update_status():
    global STATUS
    s1 = ((STATUS_RUN & 0x1) << 7) | (STATUS_BATTERY & 0x7f)
    s2 = ((STATUS_CONTROL & 0x1) << 7) | (int(STATUS_PERIOD * 10) & 0x7f)
    s3 = 0
    s4 = 0
    STATUS = (s1 << 24) | (s2 << 16) | (s3 << 8) | s4


def set_active():
    global STATUS_RUN
    STATUS_RUN = 1
    update_status()


def set_idle():
    global STATUS_RUN
    STATUS_RUN = 0
    update_status()


def change_battery(amount):
    global STATUS_BATTERY
    if amount < 0:
        STATUS_BATTERY = 0
    elif amount > 100:
        STATUS_BATTERY = 100
    else:
        STATUS_BATTERY = amount
    update_status()


def change_target(value):
    global TARGET, STATUS_CONTROL
    if TARGET != value and -20 < TARGET < 100:
        STATUS_CONTROL = 1
        TARGET = value
        update_status()


def update_current(value):
    global CURRENT
    if -20 < CURRENT < 100:
        CURRENT = value


def packet_data():
    # SERIAL, STATUS, TARGET, CURRENT 전송
    target = int(TARGET * 100)
    current = int(CURRENT * 100)
    import struct
    return struct.pack(">IIhh", SERIAL, STATUS, target, current)
