from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Smart Home IoT Cloud Engine")

device_state = {"status": "OFF"}

@app.get("/", response_class=HTMLResponse)
def web_dashboard():
    state = device_state["status"]
    color = "green" if state == "ON" else "red"
    return f"""
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
        <h2>IoT Smart Home DevOps Control v1.0</h2>
        <h3>ESP32 Load / LED: <span style="color: {color};">{state}</span></h3>
        <p><a href="/set/ON"><button style="padding: 16px 32px; font-size: 18px; background: green; color: white; border: none; border-radius: 5px;">Turn ON</button></a></p>
        <p><a href="/set/OFF"><button style="padding: 16px 32px; font-size: 18px; background: red; color: white; border: none; border-radius: 5px;">Turn OFF</button></a></p>
    </body>
    </html>
    """

@app.get("/set/{cmd}")
def switch_command(cmd: str):
    if cmd in ["ON", "OFF"]:
        device_state["status"] = cmd
    return web_dashboard()

@app.get("/api/device/status")
def device_poll():
    return device_state

@app.get("/health")
def health_check():
    return {"status": "healthy"}