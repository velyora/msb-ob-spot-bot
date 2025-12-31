import time, json, os

STATE_FILE = "state.json"

def now():
    return int(time.time())

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_sent": 0, "signals": {}}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def can_send(state, key, max_per_min, dedup_hours):
    if now() - state["last_sent"] < 60 / max_per_min:
        return False
    if key in state["signals"]:
        if now() - state["signals"][key] < dedup_hours * 3600:
            return False
    return True

def mark_sent(state, key):
    state["last_sent"] = now()
    state["signals"][key] = now()
