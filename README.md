# FastAPI Cloud App

A starter FastAPI project deployed on [FastAPI Cloud](https://fastapicloud.com).

## What is this?

This repo is a simple, production-ready FastAPI application set up for one-command deployment to FastAPI Cloud. It uses [uv](https://docs.astral.sh/uv/) as the package manager.

## Endpoints

| Method | Path      | Description              |
|--------|-----------|--------------------------|
| GET    | `/`       | Returns a welcome message |
| GET    | `/health` | Health check endpoint     |
| GET    | `/docs`   | Auto-generated Swagger UI |
| GET    | `/redoc`  | ReDoc API documentation   |

## Project Structure

```
.
├── app.py           # FastAPI application (entrypoint)
├── pyproject.toml   # Project config and dependencies
├── .python-version  # Pinned Python version
└── README.md
```

## Local Development

**Prerequisites:** Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
# Install dependencies
uv sync

# Run the dev server (auto-reloads on changes)
uv run fastapi dev

# Or run directly
uv run python app.py

# App runs at http://0.0.0.0:8000
# Swagger docs at http://0.0.0.0:8000/docs
# ReDoc at http://0.0.0.0:8000/redoc
```

## Adding Dependencies

```bash
uv add <package-name>
```

---

## Deploy to FastAPI Cloud

### Step 1: Login

```bash
uv run fastapi login
```

Opens your browser to authenticate. Create an account if you don't have one.

### Step 2: Deploy

```bash
uv run fastapi deploy
```

The CLI will:
1. Prompt you to select or create a **team**
2. Ask you to **choose an app name** — this becomes your URL
3. Package and upload your code
4. Build and deploy with zero downtime

Your app will be live at:

```
https://<your-app-name>.fastapicloud.dev
```

> **Naming rules:** Use lowercase letters, numbers, and hyphens only. No spaces or special characters.
> Examples: `my-app`, `todo-api-v2`, `coolproject`

### Step 3: Done

Visit `https://<your-app-name>.fastapicloud.dev/docs` to explore your live API.

---

## CLI Reference

All commands use `uv run fastapi <command>`.

### Authentication

```bash
# Login to FastAPI Cloud
uv run fastapi login

# Check who you're logged in as
uv run fastapi whoami

# Logout
uv run fastapi logout
```

### Deploy

```bash
# Deploy current directory
uv run fastapi deploy

# Deploy a specific path
uv run fastapi deploy ./my-app

# Deploy without waiting for completion (CI/CD)
uv run fastapi deploy --no-wait

# Deploy to a specific app by ID
uv run fastapi deploy --app-id <app-id>
```

After the first deploy, a `.fastapicloud` directory is created that links your local project to the cloud app. Subsequent deploys just need `uv run fastapi deploy`.

### Environment Variables

```bash
# List all env vars
uv run fastapi cloud env list

# Set an env var (applies on next deploy)
uv run fastapi cloud env set API_KEY "your-key"

# Set a secret (encrypted, hidden in dashboard)
uv run fastapi cloud env set --secret DATABASE_URL "postgresql://..."

# Delete an env var
uv run fastapi cloud env delete API_KEY

# Interactive mode (prompts for name and value)
uv run fastapi cloud env set
```

> **Note:** Setting env vars via CLI does NOT auto-redeploy. Changes take effect on the next deployment.
> You can also manage env vars in the [dashboard](https://dashboard.fastapicloud.com) with bulk `.env` import and instant redeploy.

### Logs

```bash
# Stream logs in real-time
uv run fastapi cloud logs

# Fetch recent logs and exit
uv run fastapi cloud logs --no-follow

# Show last 50 lines
uv run fastapi cloud logs --tail 50

# Logs from the last hour
uv run fastapi cloud logs --since 1h

# Time formats: 30s, 5m, 1h, 2d
```

### Project Linking

```bash
# Link local dir to an existing cloud app
uv run fastapi cloud link

# Remove the local link
uv run fastapi cloud unlink
```

### CI/CD (GitHub Actions)

```bash
# Auto-configure GitHub Actions for auto-deploy on push
uv run fastapi cloud setup-ci

# Target a specific branch (default: main)
uv run fastapi cloud setup-ci --branch production

# Preview without making changes
uv run fastapi cloud setup-ci --dry-run
```

This creates a GitHub Actions workflow that auto-deploys on push. It sets `FASTAPI_CLOUD_TOKEN` and `FASTAPI_CLOUD_APP_ID` as GitHub repo secrets automatically (requires `gh` CLI).

### Custom Domains

Custom domains are managed in the [dashboard](https://dashboard.fastapicloud.com):

1. Go to your app → **Domains** → **Add Custom Domain**
2. Enter your domain (e.g. `api.yourdomain.com`)
3. Add the DNS records shown (CNAME for subdomains, A records for apex)
4. TLS certificates are issued automatically

Your app stays accessible at `https://<name>.fastapicloud.dev` even with a custom domain.

---

## Useful Links

- [FastAPI Cloud Docs](https://fastapicloud.com/docs/getting-started)
- [FastAPI Cloud Dashboard](https://dashboard.fastapicloud.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [uv Docs](https://docs.astral.sh/uv)
