from dataclasses import dataclass
from typing import List

@dataclass
class BearTrapResult:
    state: str
    allowed_action: str
    reason: str


def detect_bear_trap(channel_positions: List[float], volumes: List[float] | None = None, reclaim_days: int = 5, reclaim_position: float = 0.05, l3_retreat: bool = False, l4_blowup: bool = False) -> BearTrapResult:
    """Detect bear trap reclaim after a channel undercut.

    This is causal if called with data only up to current date.
    """
    if not channel_positions:
        return BearTrapResult("UNKNOWN", "WAIT", "no channel positions")
    current = channel_positions[-1]
    recent = channel_positions[-reclaim_days:]
    undercut = any(x < 0 for x in recent)
    if not undercut:
        if current < 0.25:
            return BearTrapResult("CHANNEL_LOW_ZONE", "WATCH", "low channel zone")
        if current > 0.70:
            return BearTrapResult("HIGH_ZONE", "HARVEST", "near upper band")
        return BearTrapResult("NORMAL_ZONE", "WAIT", "not low enough")
    if l3_retreat or l4_blowup:
        return BearTrapResult("STRUCTURAL_BREAKDOWN", "WAIT", "sector or fundamentals broken")
    if current > reclaim_position:
        return BearTrapResult("BEAR_TRAP_RECLAIMED", "PAPER_PROBE", "reclaimed channel after undercut")
    return BearTrapResult("WATCH_BEAR_TRAP", "WATCH", "undercut not yet reclaimed")
