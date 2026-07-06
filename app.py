import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from modules import get_app_info, get_full_status

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

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    logger.info("GET / — rendering dashboard")
    return templates.TemplateResponse(request, "index.html")


@app.get("/info")
async def info():
    logger.info("GET /info — returning app info")
    return get_app_info()


@app.get("/health")
async def health():
    logger.info("GET /health — health check passed")
    return {"status": "ok"}


@app.get("/status")
async def status():
    logger.info("GET /status — returning system info")
    return get_full_status()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
