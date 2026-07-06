import logging
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
    get_ping_history,
    get_request_stats,
    start_pinger,
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
    {"name": "protected", "description": "Endpoints requiring X-API-Key header"},
]

app.openapi_tags = TAGS_METADATA


# --- Lifecycle ---
@app.on_event("startup")
async def startup():
    logger.info("Application starting — launching health pinger")
    start_pinger()


# --- Routes: Public ---
@app.get("/", response_class=HTMLResponse, tags=["dashboard"])
@limiter.limit("30/minute")
async def root(request: Request):
    logger.info("GET / — rendering dashboard")
    status = get_full_status()
    info = get_app_info()
    ip = await get_client_ip(request)
    geo = await get_geolocation(ip)
    pings = get_ping_history()
    return templates.TemplateResponse(request, "index.html", {
        "status": status,
        "info": info,
        "geo": geo,
        "pings": pings,
    })


@app.get("/health", tags=["dashboard"])
@limiter.limit("60/minute")
async def health(request: Request):
    logger.info("GET /health — health check passed")
    return {"status": "ok"}


# --- Routes: Monitoring ---
@app.get("/status", tags=["monitoring"])
@limiter.limit("30/minute")
async def status(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /status — returning system info")
    return get_full_status()


@app.get("/info", tags=["monitoring"])
@limiter.limit("30/minute")
async def info(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /info — returning app info")
    return get_app_info()


@app.get("/metrics", tags=["monitoring"])
@limiter.limit("30/minute")
async def metrics(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /metrics — returning request stats")
    return get_request_stats()


# --- Routes: Protected ---
@app.get("/geo", tags=["protected"])
@limiter.limit("10/minute")
async def geo(request: Request, api_key: str = Depends(require_api_key)):
    ip = await get_client_ip(request)
    logger.info(f"GET /geo — looking up {ip}")
    return await get_geolocation(ip)


@app.get("/pings", tags=["protected"])
@limiter.limit("30/minute")
async def pings(request: Request, api_key: str = Depends(require_api_key)):
    logger.info("GET /pings — returning ping history")
    return {"pings": get_ping_history()}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
