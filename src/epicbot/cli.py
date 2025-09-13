# one-shot diagnostic for Step 2: prints status and message; no posting
from .epic_feed import fetch_raw, current_free
from .fingerprint import make_fingerprint
from .state import load_state, save_state
from .message import build_message


def main() -> None:

    raw = fetch_raw()
    offers = current_free(raw)
    sig = make_fingerprint(offers)
    st = load_state()
    changed = sig != st.get("sig")
    print(f"changed={changed}  offers={len(offers)}  fingerprint={sig}")
    print("---")
    print(build_message(offers))
    if changed:
        save_state(sig)

if __name__ == "__main__":
    main()
