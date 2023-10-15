def start(client, args=None):
    client.on_message = on_message
    client.subscribe(
        "common", # 채널 토픽
        1, # QoS
    )
    client.loop_forever()

def on_message(client, userdata, msg):
    payload = msg.payload.decode("UTF-8")
    print(f"Topic[{msg.topic}]: {payload}")