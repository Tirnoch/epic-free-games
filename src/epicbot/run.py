import os, time, traceback
from .epic_feed import fetch_raw, current_free
from .fingerprint import make_fingerprint
from .state import load_state, save_state
from .message import build_message
from .discord_notify import post_to_discord


def tick() -> None:
    raw = fetch_raw()
    offers = current_free(raw)
    sig = make_fingerprint(offers)
    st = load_state()
    if sig != st.get("sig"):
        if offers:
            post_to_discord(build_message(offers))
        save_state(sig)

def main() -> None:

    interval_min = int(os.getenv("POLL_MINUTES", "60"))
    while True:
        try:
            tick()
        except Exception:
            print("tick failed:\n" + traceback.format_exc())
        time.sleep(interval_min * 60)

if __name__ == "__main__":
    main()
