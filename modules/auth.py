import os
import logging
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

logger = logging.getLogger("app.auth")

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key() -> str | None:
    return os.getenv("API_KEY")


async def require_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> str:
    expected = get_api_key()
    if not expected:
        return "no-key-configured"
    if not api_key or api_key != expected:
        logger.warning("Invalid or missing API key")
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key
