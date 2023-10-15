def on_connect(client, userdata, flags, rc):
    pass

def on_disconnect(client, userdata, flgas, rc=0):
    pass

def on_publish(cleint, userdata, mid, qos):
        print(f"Subscribed: "
              f"Message ID={mid}: QoS={qos}")