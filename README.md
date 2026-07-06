# FastAPI Cloud App

A production-ready FastAPI application deployed on [FastAPI Cloud](https://fastapicloud.com) with system monitoring, API key auth, rate limiting, geolocation, and a live dashboard.

## Features

- **Live Dashboard** — glassmorphism UI with system stats (CPU, RAM, disk, network), visitor geolocation, health pinger history, and social links
- **API Key Auth** — protected endpoints require `X-API-Key` header
- **Rate Limiting** — 60 req/min per IP (configurable per route)
- **Request Counter** — middleware tracks total requests per endpoint
- **IP Geolocation** — lookup visitor location via ip-api.com
- **Health Pinger** — background task pings a URL on a cron schedule
- **OpenAPI Customization** — custom schema with tags, descriptions, contact info

## Endpoints

| Method | Path       | Auth | Description                                    |
|--------|------------|------|------------------------------------------------|
| GET    | `/`        | No   | Live dashboard (server-rendered)               |
| GET    | `/health`  | No   | Health check                                   |
| GET    | `/status`  | Yes  | System specs: CPU, RAM, disk, network, uptime  |
| GET    | `/info`    | Yes  | App info: GitHub & LinkedIn links              |
| GET    | `/metrics` | Yes  | Request stats: total count, per-endpoint       |
| GET    | `/geo`     | Yes  | IP geolocation of the requester                |
| GET    | `/pings`   | Yes  | Health pinger history                          |
| GET    | `/docs`    | No   | Swagger UI                                     |
| GET    | `/redoc`   | No   | ReDoc                                          |

> **Auth:** Pass `X-API-Key: <your-key>` header for protected endpoints.

## Dashboard

The `/` route renders a server-side dashboard showing:

- **System metrics** — CPU, memory, disk usage with progress bars
- **System info** — OS, architecture, hostname, Python version, CPU frequency
- **Network I/O** — bytes and packets sent/received
- **Visitor geolocation** — your IP, country, city, ISP, coordinates
- **Health pinger** — last 5 pings with status codes and latency
- **Social links** — GitHub & LinkedIn from env vars

The dashboard is public (no API key needed). Data is injected server-side via Jinja2 — no client-side API calls required.

## Project Structure

```
.
├── app.py                # FastAPI routes only
├── modules/
│   ├── __init__.py       # Re-exports all module functions
│   ├── utils.py          # System info, env vars, CPU/RAM/disk/network
│   ├── auth.py           # API key dependency
│   ├── geo.py            # IP geolocation lookup
│   ├── middleware.py      # Request counter middleware
│   ├── rate_limit.py      # Slowapi rate limiter
│   ├── health_pinger.py   # Background cron health pinger
│   └── openapi.py         # Custom OpenAPI schema
├── templates/
│   └── index.html        # Dashboard UI (dark glassmorphism)
├── pyproject.toml
├── .python-version
├── .env                  # Local env vars (gitignored)
├── .env.sample           # Env template (tracked)
└── README.md
```

## Architecture

- **`app.py`** — Routes only. Imports functions from `modules`, wires middleware, starts background tasks.
- **`modules/utils.py`** — System info, env vars, CPU/RAM/disk/network helpers.
- **`modules/auth.py`** — API key dependency (`X-API-Key` header).
- **`modules/geo.py`** — Async IP geolocation via `ip-api.com`.
- **`modules/middleware.py`** — `RequestCounterMiddleware` — counts requests, logs timing.
- **`modules/rate_limit.py`** — Slowapi rate limiter instance.
- **`modules/health_pinger.py`** — APScheduler job pings a URL on a cron interval, stores history.
- **`modules/openapi.py`** — Custom OpenAPI schema with tags, descriptions, contact info.
- **`modules/__init__.py`** — Re-exports all public functions via `__all__`.

```python
from modules import get_app_info, get_full_status
```

## Local Development

**Prerequisites:** Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Install dependencies
uv sync

# Set up env vars
cp .env.sample .env
# Edit .env with your values

# Run the dev server
uv run python app.py

# App runs at http://0.0.0.0:8000
# Dashboard at http://0.0.0.0:8000
# Swagger docs at http://0.0.0.0:8000/docs
```

## Environment Variables

| Variable          | Required | Default              | Description                          |
|-------------------|----------|----------------------|--------------------------------------|
| `GITHUB_URL`      | No       | `https://github.com` | GitHub profile link                  |
| `LINKEDIN_URL`    | No       | `https://linkedin.com` | LinkedIn profile link              |
| `API_KEY`         | No       | —                    | API key for protected endpoints      |
| `PINGER_URL`      | No       | —                    | URL for health pinger to ping        |
| `PINGER_INTERVAL` | No       | `300`                | Pinger interval in seconds           |

### Local Setup

```bash
cp .env.sample .env
# Fill in your values
```

### Cloud Setup

```bash
uv run fastapi cloud env set API_KEY "your-secret-key"
uv run fastapi cloud env set GITHUB_URL "https://github.com/dhimanparas20"
uv run fastapi cloud env set LINKEDIN_URL "https://www.linkedin.com/in/dhimanparas20/"
uv run fastapi cloud env set PINGER_URL "https://your-app.fastapicloud.dev/health"
```

> **Note:** `.env` is gitignored. `.env.sample` is tracked so others know which variables are needed.

## Using Protected Endpoints

```bash
# Without API key — 401
curl http://0.0.0.0:8000/status

# With API key — 200
curl -H "X-API-Key: test123" http://0.0.0.0:8000/status

# Geolocation
curl -H "X-API-Key: test123" http://0.0.0.0:8000/geo

# Request metrics
curl -H "X-API-Key: test123" http://0.0.0.0:8000/metrics

# Ping history
curl -H "X-API-Key: test123" http://0.0.0.0:8000/pings
```

---

## Deploy to FastAPI Cloud

### Step 1: Login

```bash
uv run fastapi login
```

### Step 2: Deploy

```bash
uv run fastapi deploy
```

Pick an app name — it becomes `https://<name>.fastapicloud.dev`.

### Step 3: Set Environment Variables

```bash
uv run fastapi cloud env set API_KEY "your-production-key"
uv run fastapi cloud env set GITHUB_URL "https://github.com/dhimanparas20"
uv run fastapi cloud env set LINKEDIN_URL "https://www.linkedin.com/in/dhimanparas20/"
uv run fastapi cloud env set PINGER_URL "https://<name>.fastapicloud.dev/health"
```

---

## CLI Reference

All commands use `uv run fastapi <command>`.

### Authentication

```bash
uv run fastapi login
uv run fastapi whoami
uv run fastapi logout
```

### Deploy

```bash
uv run fastapi deploy
uv run fastapi deploy --no-wait
```

### Environment Variables

```bash
uv run fastapi cloud env list
uv run fastapi cloud env set KEY "value"
uv run fastapi cloud env set --secret KEY "value"
uv run fastapi cloud env delete KEY
```

### Logs

```bash
uv run fastapi cloud logs
uv run fastapi cloud logs --no-follow
uv run fastapi cloud logs --tail 50
uv run fastapi cloud logs --since 1h
```

### Project Linking

```bash
uv run fastapi cloud link
uv run fastapi cloud unlink
```

### CI/CD (GitHub Actions)

```bash
uv run fastapi cloud setup-ci
uv run fastapi cloud setup-ci --branch production
```

### Custom Domains

Managed in the [dashboard](https://dashboard.fastapicloud.com) → your app → Domains.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi[standard]` | Web framework + CLI + uvicorn |
| `psutil` | System metrics (CPU, RAM, disk, network) |
| `slowapi` | Rate limiting middleware |
| `httpx` | Async HTTP client (geolocation + pinger) |
| `python-dotenv` | Load `.env` files |
| `jinja2` | HTML template rendering |
| `apscheduler` | Cron-style health pinger scheduler |

## Useful Links

- [FastAPI Cloud Docs](https://fastapicloud.com/docs/getting-started)
- [FastAPI Cloud Dashboard](https://dashboard.fastapicloud.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [uv Docs](https://docs.astral.sh/uv)
- [slowapi Docs](https://github.com/laurentS/slowapi)
