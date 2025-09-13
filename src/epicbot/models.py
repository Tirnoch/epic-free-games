from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Offer:
    title: str
    slug_or_id: str
    namespace: str
    start_utc: str
    end_utc: str
    offer_type: str | None = None
    seller: str | None = None
    has_slug: bool = True