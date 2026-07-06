import asyncio
import logging
import os
from datetime import datetime, timezone

import httpx

logger = logging.getLogger("app.pinger")

PINGER_INTERVAL_SECONDS = int(os.getenv("PINGER_INTERVAL", "300"))
PINGER_URL = os.getenv("PINGER_URL")

ping_history: list[dict] = []
MAX_HISTORY = 100


async def _ping_once(url: str) -> dict:
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "url": url}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            entry["status_code"] = resp.status_code
            entry["ok"] = resp.status_code == 200
            entry["latency_ms"] = round(resp.elapsed.total_seconds() * 1000, 2)
    except Exception as e:
        entry["status_code"] = None
        entry["ok"] = False
        entry["error"] = str(e)

    logger.info(f"Ping {url} → {'OK' if entry['ok'] else 'FAIL'} ({entry.get('status_code')})")
    return entry


async def health_pinger_task():
    if not PINGER_URL:
        logger.info("PINGER_URL not set, health pinger disabled")
        return

    logger.info(f"Health pinger started — pinging {PINGER_URL} every {PINGER_INTERVAL_SECONDS}s")
    await asyncio.sleep(5)

    while True:
        result = await _ping_once(PINGER_URL)
        ping_history.append(result)
        if len(ping_history) > MAX_HISTORY:
            ping_history.pop(0)
        await asyncio.sleep(PINGER_INTERVAL_SECONDS)


def get_ping_history() -> list[dict]:
    return ping_history
