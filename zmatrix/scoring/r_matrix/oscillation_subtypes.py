from enum import Enum

class OscillationType(str, Enum):
    """Oscillation subtypes for R-Matrix."""
    HORIZONTAL = "OSC_TYPE_A_HORIZONTAL"
    RISING_CHANNEL = "OSC_TYPE_B_RISING_CHANNEL"

class OscillationAction(str, Enum):
    WATCH = "WATCH"
    WAIT = "WAIT"
    PAPER_PROBE = "PAPER_PROBE"
    HARVEST = "HARVEST"

FORBIDDEN_ACTIONS = {"BUY", "ADD", "HEAVY_POSITION", "CLEAR", "AUTO_ENTER"}
ALLOWED_ACTIONS = {a.value for a in OscillationAction}

def assert_allowed_action(action: str) -> None:
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"OscillationKingRanker may not output action={action}")
