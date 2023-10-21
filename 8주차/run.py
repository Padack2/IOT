def start(client):
    import threading
    import device.measure as measure
    t = threading.Thread(target=measure.measure_loop, daemon=True)
    t.start()

    import device.control as control
    t = threading.Thread(target=control.start, args=(client,), daemon=True)
    t.start()

    import device.transport as transport
    transport.setup(client)
    transport.report_start(client)
