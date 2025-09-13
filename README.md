# epic-free-webhook

Posts Epic Games weekly free games to a Discord channel via webhook.  
Checks hourly (configurable). Posts only when the free set changes.  
No inbound ports.

## Quick start

```bash
# 1) Clone
git clone https://github.com/Tirnoch/epic-free-games.git ~/apps/epic-free-games
cd ~/apps/epic-free-games

# 2) Create .env from template
cp .env.sample .env
# edit .env and paste your Discord webhook URL (no quotes)

# 3) Build and start
docker compose up -d --build

# 4) Logs
docker compose logs -f epic-free-webhook
```

## docker-compose.yml

```yaml
services:
  epic-free-webhook:
    build: .
    image: epic-free-webhook:latest
    environment:
      DISCORD_WEBHOOK_URL: ${DISCORD_WEBHOOK_URL}
      EPIC_COUNTRY: ${EPIC_COUNTRY:-TR}
      EPIC_LOCALE: ${EPIC_LOCALE:-en-US}
      POLL_MINUTES: ${POLL_MINUTES:-60}
      STATE_PATH: /data/epic_state.json
    volumes:
      - epic_free_state:/data
    restart: unless-stopped
volumes:
  epic_free_state:
```

## Dockerfile

```dockerfile
FROM python:3.12-slim
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
ENV STATE_PATH=/data/epic_state.json POLL_MINUTES=60
CMD ["python", "-m", "epicbot.run"]

```

## .dockerignore

```dockerignore
.venv/
.state/
.env
.env.*
!.env.sample
__pycache__/
*.py[cod]
*.log
.git
.gitignore
dist/
build/
*.egg-info/
.eggs/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.pyright/
.vscode/
.idea/
.DS_Store
Thumbs.db
```

## .env.sample

```ini
DISCORD_WEBHOOK_URL=
EPIC_COUNTRY=TR
EPIC_LOCALE=en-US
POLL_MINUTES=60
```

## Operations

```bash
# status
docker compose ps

# follow logs
docker compose logs -f epic-free-webhook

# force one-time post
docker compose exec -T epic-free-webhook sh -lc 'rm -f /data/epic_state.json'
docker compose exec -T epic-free-webhook python -c "from epicbot.run import tick; tick()"

# restart after code or env changes
docker compose up -d --build

# stop / remove
docker compose stop
docker compose down
```
