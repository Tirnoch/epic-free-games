# epic-free-webhook

Posts Epic Games weekly free games to a Discord channel via webhook. Polls hourly. No inbound ports.

## Quick start (Docker Compose)

```bash
# 1) Clone
git clone https://github.com/Tirnoch/epic-free-games.git ~/apps/epic-free-webhook
cd ~/apps/epic-free-webhook

# 2) Create Compose env (gitignored)
cat > .env <<'ENV'
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
EPIC_COUNTRY=TR
EPIC_LOCALE=en-US
POLL_MINUTES=60
ENV

# 3) Bring it up
docker compose up -d --build

# 4) Check logs
docker compose logs -f
```
