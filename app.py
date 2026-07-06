import logging
import os
import platform
from datetime import datetime, timezone

import psutil
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("app")

app = FastAPI(
    title="FastAPI Cloud App",
    version="0.1.0",
    description="A production-ready FastAPI app deployed on FastAPI Cloud",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


@app.get("/")
async def root():
    logger.info("GET / — returning welcome message")
    return {
        "message": "Hello World",
        "github": os.getenv("GITHUB_URL", "https://github.com"),
        "linkedin": os.getenv("LINKEDIN_URL", "https://www.linkedin.com"),
    }


@app.get("/status")
async def status():
    logger.info("GET /status — returning system info")
    cpu_percent = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    boot_time = datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "uptime_seconds": (datetime.now(timezone.utc) - boot_time).total_seconds(),
        },
        "cpu": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "usage_percent": cpu_percent,
            "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
        },
        "memory": {
            "total_mb": round(memory.total / (1024**2), 2),
            "available_mb": round(memory.available / (1024**2), 2),
            "used_mb": round(memory.used / (1024**2), 2),
            "usage_percent": memory.percent,
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "usage_percent": round(disk.percent, 2),
        },
        "network": {
            "bytes_sent": net.bytes_sent,
            "bytes_received": net.bytes_recv,
            "packets_sent": net.packets_sent,
            "packets_received": net.packets_recv,
        },
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
