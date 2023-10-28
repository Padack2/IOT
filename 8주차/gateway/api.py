from gateway.server import (
    run_manager_thread, run_message_thread,
    create_client)

run_manager_thread()
run_message_thread(create_client())
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/device")
def list_devices():
    from gateway import devices
    items = []
    for dev in devices.DEVICES.values():
        items.append({
            "serial": dev.serial, "type": dev.type, "status": dev.status
        })
    return {
        "items": items
    }


from typing import Optional
from fastapi import HTTPException


@app.get("/api/device/{device}")
def read_device(device: int, q: Optional[str] = None):
    from gateway import devices
    if not devices.is_exists(device):
        raise HTTPException(status_code=404, detail="Device not found")
    dev = devices.DEVICES[device]
    return {
        "serial": dev.serial, "type": dev.type, "status": dev.status,
        "extra": dev.extra
    }


@app.get("/api/device/{device}/control")
def control_device(device: int, t: Optional[str] = None):
    if t is None:
        return {"result": "failed", "reason": "t value not provided"}
    # 여기에 온도 제어 프로그램 두기
    return {"result": "success"}
