import logging
import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.middleware")

request_counts: dict[str, int] = defaultdict(int)
total_requests = 0


class RequestCounterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        global total_requests
        path = request.url.path
        method = request.method

        total_requests += 1
        request_counts[f"{method} {path}"] += 1

        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)

        logger.info(f"{method} {path} → {response.status_code} ({duration}ms)")
        response.headers["X-Request-Count"] = str(total_requests)

        return response


def get_request_stats() -> dict:
    return {
        "total_requests": total_requests,
        "endpoints": dict(request_counts),
    }
