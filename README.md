# FastAPI Cloud App

A production-ready FastAPI application with system monitoring, API key auth, rate limiting, geolocation, and a live dashboard.

## Live Deployments

| Platform | URL |
|----------|-----|
| FastAPI Cloud | https://mst-fastapi-cloud-f92a3a85.fastapicloud.dev/ |
| Vercel (Docker) | https://fastapi-cloud.vercel.app/ |

## Features

- **Live Dashboard** — glassmorphism UI with lazy-loaded system stats, visitor geolocation, and social links
- **API Key Auth** — all `/api/*` endpoints require `X-API-Key` header
- **Rate Limiting** — 60 req/min per IP (configurable per route)
- **Request Counter** — middleware tracks total requests per endpoint
- **IP Geolocation** — lookup visitor location via ip-api.com
- **OpenAPI Customization** — custom schema with tags, descriptions, contact info

## Endpoints

| Method | Path           | Auth | Description                                    |
|--------|----------------|------|------------------------------------------------|
| GET    | `/`            | No   | Live dashboard (lazy-loads data via JS)        |
| GET    | `/health`      | No   | Health check                                   |
| GET    | `/api/status`  | Yes  | System specs: CPU, RAM, disk, network, uptime  |
| GET    | `/api/info`    | Yes  | App info: GitHub & LinkedIn links              |
| GET    | `/api/geo`     | Yes  | IP geolocation of the requester                |
| GET    | `/api/metrics` | Yes  | Request stats: total count, per-endpoint       |
| GET    | `/docs`        | No   | Swagger UI                                     |
| GET    | `/redoc`       | No   | ReDoc                                          |

> **Auth:** Pass `X-API-Key: <your-key>` header for protected endpoints.
> The dashboard automatically receives the API key from the backend and uses it for lazy-loading.

## Dashboard

The `/` route renders a fully client-side dashboard:

1. Page loads instantly with **spinner placeholders** in all sections
2. Three parallel `fetch()` calls fire to `/api/status`, `/api/info`, `/api/geo`
3. Each section fills in as its data arrives
4. If a request fails, shows "Failed to load" gracefully

Sections: system metrics, system info, network I/O, visitor geolocation, social links.

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
│   └── openapi.py         # Custom OpenAPI schema
├── templates/
│   └── index.html        # Dashboard UI (dark glassmorphism)
├── Dockerfile            # FastAPI Cloud container image
├── Dockerfile.vercel     # Vercel container image
├── compose.yml           # Docker Compose config
├── .dockerignore         # Docker build exclusions
├── pyproject.toml
├── .python-version
├── .env                  # Local env vars (gitignored)
├── .env.sample           # Env template (tracked)
└── README.md
```

## Architecture

- **`app.py`** — Routes only. Passes API key to template, wires middleware.
- **`modules/utils.py`** — System info, env vars, CPU/RAM/disk/network helpers.
- **`modules/auth.py`** — API key dependency (`X-API-Key` header).
- **`modules/geo.py`** — Async IP geolocation via `ip-api.com`.
- **`modules/middleware.py`** — `RequestCounterMiddleware` — counts requests, logs timing.
- **`modules/rate_limit.py`** — Slowapi rate limiter instance.
- **`modules/openapi.py`** — Custom OpenAPI schema with tags, descriptions, contact info.
- **`modules/__init__.py`** — Re-exports all public functions via `__all__`.

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

| Variable       | Required | Default                | Description                       |
|----------------|----------|------------------------|-----------------------------------|
| `GITHUB_URL`   | No       | `https://github.com`   | GitHub profile link               |
| `LINKEDIN_URL` | No       | `https://linkedin.com` | LinkedIn profile link             |
| `API_KEY`      | No       | —                      | API key for protected endpoints   |

### Local Setup

```bash
cp .env.sample .env
# Fill in your values
```

### Cloud Setup

```bash
# FastAPI Cloud
uv run fastapi cloud env set API_KEY "your-secret-key"
uv run fastapi cloud env set GITHUB_URL "https://github.com/dhimanparas20"
uv run fastapi cloud env set LINKEDIN_URL "https://www.linkedin.com/in/dhimanparas20/"

# Vercel — set env vars in the Vercel dashboard
```

> **Note:** `.env` is gitignored. `.env.sample` is tracked so others know which variables are needed.

## Using Protected Endpoints

```bash
# Without API key — 401
curl https://mst-fastapi-cloud-f92a3a85.fastapicloud.dev/api/status

# With API key — 200
curl -H "X-API-Key: your-key" https://mst-fastapi-cloud-f92a3a85.fastapicloud.dev/api/status

# Geolocation
curl -H "X-API-Key: your-key" https://mst-fastapi-cloud-f92a3a85.fastapicloud.dev/api/geo

# Request metrics
curl -H "X-API-Key: your-key" https://mst-fastapi-cloud-f92a3a85.fastapicloud.dev/api/metrics
```

---

## Deploy to FastAPI Cloud

```bash
uv run fastapi login
uv run fastapi deploy
```

Pick an app name — it becomes `https://<name>.fastapicloud.dev`.

### Set Environment Variables

```bash
uv run fastapi cloud env set API_KEY "your-production-key"
uv run fastapi cloud env set GITHUB_URL "https://github.com/dhimanparas20"
uv run fastapi cloud env set LINKEDIN_URL "https://www.linkedin.com/in/dhimanparas20/"
```

---

## Deploy to Vercel

Using `Dockerfile.vercel`:

```bash
vercel --prod
```

Set environment variables in the Vercel dashboard → Settings → Environment Variables.

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

### Custom Domains

Managed in the [dashboard](https://dashboard.fastapicloud.com) → your app → Domains.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi[standard]` | Web framework + CLI + uvicorn |
| `psutil` | System metrics (CPU, RAM, disk, network) |
| `slowapi` | Rate limiting middleware |
| `httpx` | Async HTTP client (geolocation) |
| `python-dotenv` | Load `.env` files |
| `jinja2` | HTML template rendering |

## Docker

```bash
# Build and run
docker build -t fastapi-cloud .
docker run -p 8000:8000 --env-file .env fastapi-cloud

# Docker Compose
docker compose up -d
docker compose logs -f
docker compose down
```

## Useful Links

- [FastAPI Cloud Docs](https://fastapicloud.com/docs/getting-started)
- [FastAPI Cloud Dashboard](https://dashboard.fastapicloud.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [uv Docs](https://docs.astral.sh/uv)
- [slowapi Docs](https://github.com/laurentS/slowapi)
