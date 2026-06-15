"""Event Calendar Provider — read-only macro event data loader."""
from pathlib import Path
import json
from datetime import date

def load_event_context(ticker: str, today: date) -> dict:
    src = Path("data/examples/event_calendar.example.json")
    if not src.exists():
        return _no_event()
    try:
        data = json.loads(src.read_text())
        events = data.get("events", [])
        for ev in events:
            ev_date = date.fromisoformat(ev.get("date", "2000-01-01"))
            delta = (ev_date - today).days
            sev = ev.get("risk_severity", "none")
            if sev == "blackswans" and delta <= 1:
                return {"event_window_active": True, "event_type": ev.get("type"),
                        "event_risk_severity": "blackswans", "event_phase": "event_day",
                        "event_expected": False, "event_confirmation_received": False}
            if sev == "scheduled" and -2 <= delta <= 2:
                phase = { -2:"pre_2d", -1:"pre_1d", 0:"event_day" }.get(delta, "post_48h")
                return {"event_window_active": True, "event_type": ev.get("type"),
                        "event_risk_severity": "scheduled", "event_phase": phase,
                        "event_expected": True, "event_confirmation_received": delta > 0}
        return _no_event()
    except (json.JSONDecodeError, KeyError, OSError):
        return _no_event()

def _no_event() -> dict:
    return {"event_window_active": False, "event_type": None, "event_risk_severity": "none",
            "event_phase": "none", "event_expected": False, "event_confirmation_received": False}
