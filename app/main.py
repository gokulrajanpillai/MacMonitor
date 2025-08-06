from fastapi import FastAPI, Response
from prometheus_client import Gauge, generate_latest
import psutil
import platform

app = FastAPI()

cpu_usage = Gauge('mac_cpu_usage_percent', 'CPU Usage Percent')
ram_usage = Gauge('mac_ram_usage_bytes', 'RAM Usage Bytes')

@app.get("/metrics")
def metrics():
    cpu_usage.set(psutil.cpu_percent())
    ram_usage.set(psutil.virtual_memory().used)
    return Response(generate_latest(), media_type="text/plain")

@app.get("/hello")
def hello():
    return {"message": "Hello, Mac Monitor!"}

@app.get("/system_info")
def system_info():
    info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "ram_total": psutil.virtual_memory().total,
        "ram_available": psutil.virtual_memory().available,
    }
    return info