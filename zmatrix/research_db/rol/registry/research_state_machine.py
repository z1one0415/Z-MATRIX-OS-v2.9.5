"""R1: Research State Machine — ACTIVE→WATCHLIST→VALIDATING→WINNER/LOSER→RETIRED."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class ResearchState(str, Enum): ACTIVE="ACTIVE"; WATCHLIST="WATCHLIST"; VALIDATING="VALIDATING"; WINNER="WINNER"; LOSER="LOSER"; RETIRED="RETIRED"

TRANSITIONS = {ResearchState.ACTIVE: [ResearchState.WATCHLIST, ResearchState.VALIDATING],
    ResearchState.WATCHLIST: [ResearchState.VALIDATING, ResearchState.RETIRED],
    ResearchState.VALIDATING: [ResearchState.WINNER, ResearchState.LOSER],
    ResearchState.WINNER: [ResearchState.RETIRED], ResearchState.LOSER: [ResearchState.RETIRED], ResearchState.RETIRED: []}

@dataclass
class StateTransition:
    entry_id: str; from_state: str; to_state: str; reason: str = ""; timestamp: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchStateMachine:
    def __init__(self): self._states: dict[str, str] = {}; self._history: list[StateTransition] = []
    def init_state(self, entry_id: str, state: str = "ACTIVE"): self._states[entry_id] = state
    def transition(self, entry_id: str, to_state: str, reason: str = "") -> StateTransition | None:
        current = self._states.get(entry_id, ResearchState.ACTIVE.value)
        if to_state not in [s.value for s in (TRANSITIONS.get(ResearchState(current), []))]: return None
        from datetime import datetime, timezone
        t = StateTransition(entry_id=entry_id, from_state=current, to_state=to_state, reason=reason, timestamp=datetime.now(timezone.utc).isoformat())
        self._states[entry_id] = to_state; self._history.append(t); return t
    def get_state(self, entry_id: str) -> str: return self._states.get(entry_id, ResearchState.ACTIVE.value)
    def history(self, entry_id: str) -> list[StateTransition]: return [h for h in self._history if h.entry_id==entry_id]
