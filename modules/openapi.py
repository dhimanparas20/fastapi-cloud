from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title="FastAPI Cloud App",
        version="0.1.0",
        description=(
            "A production-ready FastAPI application deployed on FastAPI Cloud.\n\n"
            "## Features\n"
            "- **System monitoring** — CPU, memory, disk, network stats\n"
            "- **Geolocation** — IP-based visitor location lookup\n"
            "- **Request metrics** — live request counters per endpoint\n"
            "- **Health pinger** — background cron-style health checks\n"
            "- **Rate limiting** — 60 requests/minute per IP\n"
            "- **API key auth** — protected endpoints require `X-API-Key` header\n"
        ),
        routes=app.routes,
    )

    schema["info"]["contact"] = {
        "name": "GitHub",
        "url": "https://github.com/dhimanparas20/fastapi-cloud",
    }
    schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = schema
    return schema
