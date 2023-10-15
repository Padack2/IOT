def rand_error():
    import random
    value = random.randrange(-30, 30, 1)
    return value / 100


def measure():
    import device.data as data
    return data.CURRENT + rand_error()


def measure_loop():
    import time
    import device.data as data
    data.update_status()
    history = []
    while data.STATUS_RUN:
        value = measure()
        history.append(value)
        if len(history) > 5:
            history.pop(0)
        data.CURRENT = sum(history) / len(history)
        time.sleep(max(0.1, data.STATUS_PERIOD))
