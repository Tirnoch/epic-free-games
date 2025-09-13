import os, json
from typing import Any, Dict

def _state_path() -> str:
    path = os.getenv("STATE_PATH", ".state/epic_state.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def load_state() -> Dict[str, Any]:
    try:
        with open(_state_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def save_state(sig: str) -> None:
    with open(_state_path(), "w", encoding="utf-8") as f:
        json.dump({"sig": sig}, f)
