# epic-free-webhook

Posts Epic Games weekly free games to a Discord channel via webhook. Polls hourly by default. No inbound ports. Safe to run alongside other containers.

## Quick start (one-liners)

```bash
# 1) Clone
git clone https://github.com/Tirnoch/epic-free-games.git ~/apps/epic-free-webhook
cd ~/apps/epic-free-webhook

# 2) Build image
docker build -t epic-free-webhook:latest .

# 3a) Test run for 1 minute interval (prints logs, Ctrl+C to stop)
docker run --rm \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/xxx/yyy" \
  -e EPIC_COUNTRY=TR -e EPIC_LOCALE=en-US \
  -e POLL_MINUTES=1 \
  -v epic_free_state:/data \
  epic-free-webhook:latest

# 3b) Deploy detached, hourly, auto-restart
docker run -d \
  --name epic-free-webhook \
  --restart unless-stopped \
  -e DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/xxx/yyy" \
  -e EPIC_COUNTRY=TR -e EPIC_LOCALE=en-US \
  -e POLL_MINUTES=60 \
  -v epic_free_state:/data \
  epic-free-webhook:latest
```
