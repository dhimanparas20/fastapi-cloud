import logging

from fastapi import FastAPI
import uvicorn

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
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    logger.info("GET /health — health check passed")
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
