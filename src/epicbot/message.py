from typing import Iterable
from .models import Offer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.parse import quote_plus


IST = ZoneInfo("Europe/Istanbul")

def fmt_tr(iso_utc: str) -> str:
    # Epic gives Z or .000Z; make it ISO-friendly
    dt_utc = datetime.fromisoformat(iso_utc.replace("Z", "+00:00")).astimezone(timezone.utc)
    dt_tr  = dt_utc.astimezone(IST)
    # Example: 2025-09-18 18:00 TRT (UTC+0300)
    return dt_tr.strftime("%Y-%m-%d %H:%M")

def build_message(offers: Iterable[Offer]) -> str:
    offers = list(offers)
    header = f"**Epic Weekly Free Games** ({len(offers)})"
    lines = [header]
    for o in offers:
        url = (
    f"https://store.epicgames.com/en-US/p/{o.slug_or_id}"
    if o.has_slug
    else f"https://store.epicgames.com/en-US/browse?q={quote_plus(o.title)}"
)
        extra = []
        if o.offer_type: extra.append(o.offer_type)
        if o.seller: extra.append(o.seller)
        meta = f" ({', '.join(extra)})" if extra else ""
        lines.append(f"• **{o.title}** — ends {fmt_tr(o.end_utc)}\n{url}")
    return "\n".join(lines)
