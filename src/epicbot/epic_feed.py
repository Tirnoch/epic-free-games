import os
import requests
from datetime import datetime, timezone
from typing import Iterable, List, Dict, Any
from .models import Offer

BASE = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions"

def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()
def _best_slug(el: dict) -> str | None:
    # strongest to weakest
    for k in ("productSlug", "urlSlug"):
        v = el.get(k)
        if v: 
            return v
    for m in ((el.get("catalogNs") or {}).get("mappings") or []):
        if m.get("pageSlug"):
            return m["pageSlug"]
    for m in (el.get("offerMappings") or []):
        if m.get("pageSlug"):
            return m["pageSlug"]
    return None
def fetch_raw() -> Dict[str, Any]:
    locale = os.getenv("EPIC_LOCALE", "en-US")
    country = os.getenv("EPIC_COUNTRY", "US")
    url = f"{BASE}?locale={locale}&country={country}"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def _iter_elements(doc: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    return (
        doc.get("data", {})
           .get("Catalog", {})
           .get("searchStore", {})
           .get("elements", [])
        or []
    )

def current_free(doc: Dict[str, Any]) -> List[Offer]:
    now = _now_iso_utc()
    out: List[Offer] = []

    for el in _iter_elements(doc):
        promos = (el.get("promotions") or {}).get("promotionalOffers") or []
        for blk in promos:
            for p in blk.get("promotionalOffers", []):
                s, e = p.get("startDate"), p.get("endDate")
                if not (s and e): 
                    continue
                if not (s <= now < e):
                    continue
                # Free = 100% off → discountPercentage==0 means price cut to 0
                if (p.get("discountSetting") or {}).get("discountPercentage", 0) != 0:
                    continue

                slug = _best_slug(el)
                slug_or_id = slug or el.get("id") or ""
                has_slug = slug is not None

                mappings = el.get("offerMappings") or []
                if mappings:
                    slug = mappings[0].get("pageSlug") or mappings[0].get("pageId")
                slug_or_id = slug or el.get("id") or ""

                out.append(Offer(
                    title = el.get("title") or "Unknown",
                    slug_or_id = slug_or_id,
                    namespace = el.get("namespace") or "",
                    start_utc = s,
                    end_utc = e,
                    offer_type = el.get("offerType"),
                    seller = (el.get("seller") or {}).get("name"),
                    has_slug = has_slug
                ))
    # De-dup by (namespace, slug_or_id, end_utc)
    seen = set()
    uniq: List[Offer] = []
    for o in out:
        key = (o.namespace, o.slug_or_id, o.end_utc)
        if key in seen: 
            continue
        seen.add(key)
        uniq.append(o)
    return uniq
