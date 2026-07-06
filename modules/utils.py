import os
import platform
from datetime import datetime, timezone

import psutil


def get_app_info() -> dict:
    return {
        "message": "Hello World",
        "github": os.getenv("GITHUB_URL", "https://github.com"),
        "linkedin": os.getenv("LINKEDIN_URL", "https://www.linkedin.com"),
    }


def get_system_info() -> dict:
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
    }


def get_cpu_info() -> dict:
    freq = psutil.cpu_freq()
    return {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "usage_percent": psutil.cpu_percent(interval=0.5),
        "frequency_mhz": round(freq.current, 2) if freq else None,
    }


def get_memory_info() -> dict:
    mem = psutil.virtual_memory()
    return {
        "total_mb": round(mem.total / (1024**2), 2),
        "available_mb": round(mem.available / (1024**2), 2),
        "used_mb": round(mem.used / (1024**2), 2),
        "usage_percent": mem.percent,
    }


def get_disk_info() -> dict:
    disk = psutil.disk_usage("/")
    return {
        "total_gb": round(disk.total / (1024**3), 2),
        "used_gb": round(disk.used / (1024**3), 2),
        "free_gb": round(disk.free / (1024**3), 2),
        "usage_percent": round(disk.percent, 2),
    }


def get_network_info() -> dict:
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent,
        "bytes_received": net.bytes_recv,
        "packets_sent": net.packets_sent,
        "packets_received": net.packets_recv,
    }


def get_uptime_seconds() -> float:
    boot = datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)
    return (datetime.now(timezone.utc) - boot).total_seconds()


def get_full_status() -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {**get_system_info(), "uptime_seconds": get_uptime_seconds()},
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
    }
