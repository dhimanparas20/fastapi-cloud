import httpx
import logging
from fastapi import Request

logger = logging.getLogger("app.geo")

IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,lat,lon,timezone,isp,org,as,query"


async def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def get_geolocation(ip: str) -> dict:
    if ip in ("127.0.0.1", "::1", "unknown"):
        return {
            "ip": ip,
            "country": "Local",
            "city": "Localhost",
            "isp": "Loopback",
            "lat": None,
            "lon": None,
        }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(IP_API_URL.format(ip=ip))
            data = resp.json()
            if data.get("status") == "success":
                return {
                    "ip": data.get("query", ip),
                    "country": data.get("country"),
                    "country_code": data.get("countryCode"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "timezone": data.get("timezone"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "as": data.get("as"),
                }
    except Exception as e:
        logger.warning(f"Geolocation lookup failed for {ip}: {e}")

    return {"ip": ip, "country": "Unknown", "city": "Unknown", "isp": "Unknown"}
