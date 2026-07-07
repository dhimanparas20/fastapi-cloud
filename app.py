import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from modules import (
    RequestCounterMiddleware,
    custom_openapi,
    get_app_info,
    get_client_ip,
    get_full_status,
    get_geolocation,
    get_request_stats,
    limiter,
    require_api_key,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("app")

# --- App setup ---
app = FastAPI(
    title="FastAPI Cloud App",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware ---
app.state.limiter = limiter
app.add_middleware(RequestCounterMiddleware)

# --- OpenAPI ---
app.openapi = lambda: custom_openapi(app)

# --- Templates ---
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# --- Tags ---
TAGS_METADATA = [
    {"name": "dashboard", "description": "HTML dashboard and public endpoints"},
    {"name": "monitoring", "description": "System metrics and request stats"},
]

app.openapi_tags = TAGS_METADATA


# --- Routes: Dashboard ---
@app.get("/", response_class=HTMLResponse, tags=["dashboard"])
@limiter.limit("30/minute")
async def root(request: Request):
    logger.info("GET / — rendering dashboard")
    api_key = os.getenv("API_KEY", "")
    return templates.TemplateResponse(request, "index.html", {"api_key": api_key})


@app.get("/health", tags=["dashboard"])
@limiter.limit("60/minute")
async def health(request: Request):
    logger.info("GET /health — health check passed")
    return {"status": "ok"}


# --- Routes: API (protected) ---
@app.get("/api/status", tags=["monitoring"])
@limiter.limit("30/minute")
async def api_status(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /api/status — returning system info")
    return get_full_status()


@app.get("/api/info", tags=["monitoring"])
@limiter.limit("30/minute")
async def api_info(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /api/info — returning app info")
    return get_app_info()


@app.get("/api/geo", tags=["monitoring"])
@limiter.limit("10/minute")
async def api_geo(request: Request, api_key: str = Depends(require_api_key)):
    ip = await get_client_ip(request)
    logger.info(f"GET /api/geo — looking up {ip}")
    return await get_geolocation(ip)


@app.get("/api/metrics", tags=["monitoring"])
@limiter.limit("30/minute")
async def api_metrics(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /api/metrics — returning request stats")
    return get_request_stats()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
