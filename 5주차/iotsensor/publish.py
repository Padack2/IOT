def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK")
    else:
        print(f"Bad connection returend code={rc}")

def on_disconnect(client, userdata, flgas, rc=0):
    print(f"Disconnected(code={rc})")

def on_publish(cleint, userdata, mid):
    print(f"In publish, Message ID{mid}")