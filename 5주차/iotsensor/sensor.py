import json
import time

def start(client, args=None):
    client.loop_start()
    for v in range(10):
        client.publish(
            "common",
            json.dumps({
                "reported": {
                    "temperature": {"value": 20 + v, "unit": "C"}
                }
            }), # Message
            1 # QoS
        )
        time.sleep(5)
    client.loop_stop()