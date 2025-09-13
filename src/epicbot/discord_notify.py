import os, requests

def post_to_discord(content: str) -> None:
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        raise RuntimeError("DISCORD_WEBHOOK_URL not set")
    r = requests.post(url, json={"content": content}, timeout=10)
    if r.status_code >= 300:
        raise RuntimeError(f"Discord webhook error: {r.status_code} {r.text[:200]}")
