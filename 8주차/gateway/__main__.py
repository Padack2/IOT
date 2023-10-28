import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# import paho.mqtt.client as mqtt
# from gateway.server import start
#
# client = mqtt.Client()
# client.connect("localhost", 1883)
# start(client)
# client.disconnect()

# import paho.mqtt.client as mqtt
# from gateway.server import start, manager
# import threading
#
# t = threading.Thread(target=manager, daemon=True)
# t.start()
#
# client = mqtt.Client()
# client.connect("localhost", 1883)
# start(client)
# client.disconnect()

from gateway.server import (
    run_manager_thread, create_client, start)

run_manager_thread()
start(create_client())
