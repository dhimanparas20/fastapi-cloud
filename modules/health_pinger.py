import logging
import os
from datetime import datetime, timezone

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("app.pinger")

PINGER_INTERVAL_SECONDS = int(os.getenv("PINGER_INTERVAL", "300"))
PINGER_URL = os.getenv("PINGER_URL")

ping_history: list[dict] = []
MAX_HISTORY = 100

scheduler = AsyncIOScheduler()


async def _ping_once() -> None:
    if not PINGER_URL:
        return

    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "url": PINGER_URL}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(PINGER_URL)
            entry["status_code"] = resp.status_code
            entry["ok"] = resp.status_code == 200
            entry["latency_ms"] = round(resp.elapsed.total_seconds() * 1000, 2)
    except Exception as e:
        entry["status_code"] = None
        entry["ok"] = False
        entry["error"] = str(e)

    logger.info(f"Ping {PINGER_URL} → {'OK' if entry['ok'] else 'FAIL'} ({entry.get('status_code')})")

    ping_history.append(entry)
    if len(ping_history) > MAX_HISTORY:
        ping_history.pop(0)


def start_pinger() -> None:
    if not PINGER_URL:
        logger.info("PINGER_URL not set, health pinger disabled")
        return

    scheduler.add_job(
        _ping_once,
        "interval",
        seconds=PINGER_INTERVAL_SECONDS,
        id="health_pinger",
        name="Health Pinger",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Health pinger started — pinging {PINGER_URL} every {PINGER_INTERVAL_SECONDS}s")


def get_ping_history() -> list[dict]:
    return ping_history
