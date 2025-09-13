import hashlib
from typing import Iterable
from .models import Offer

def make_fingerprint(offers: Iterable[Offer]) -> str:
    parts = [f"{o.namespace}:{o.slug_or_id}:{o.end_utc}" for o in offers]
    parts.sort()
    joined = "|".join(parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()
