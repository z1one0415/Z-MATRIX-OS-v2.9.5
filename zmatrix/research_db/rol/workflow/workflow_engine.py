"""R3: Workflow Engine — Idea→Research→Validation→Council→Approved→Monitor→Retire."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class WorkflowStage(str, Enum): IDEA="IDEA"; RESEARCH="RESEARCH"; VALIDATION="VALIDATION"; COUNCIL="COUNCIL"; APPROVED="APPROVED"; MONITOR="MONITOR"; RETIRED="RETIRED"

WORKFLOW_ORDER = [WorkflowStage.IDEA, WorkflowStage.RESEARCH, WorkflowStage.VALIDATION, WorkflowStage.COUNCIL, WorkflowStage.APPROVED, WorkflowStage.MONITOR, WorkflowStage.RETIRED]

@dataclass
class WorkflowStep:
    step_id: str; entry_id: str; stage: str; status: str = "PENDING"; completed_at: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class WorkflowEngine:
    def __init__(self): self._workflows: dict[str, list[WorkflowStep]] = {}; self._current: dict[str, int] = {}
    def init(self, entry_id: str):
        steps = [WorkflowStep(step_id=f"{entry_id}-{s.value}", entry_id=entry_id, stage=s.value) for s in WORKFLOW_ORDER]
        self._workflows[entry_id] = steps; self._current[entry_id] = 0; steps[0].status = "ACTIVE"
    def advance(self, entry_id: str) -> WorkflowStep | None:
        i = self._current.get(entry_id, -1)
        if i < 0 or i + 1 >= len(self._workflows.get(entry_id, [])): return None
        self._workflows[entry_id][i].status = "COMPLETED"; self._workflows[entry_id][i].completed_at = datetime.now(timezone.utc).isoformat()
        self._current[entry_id] = i + 1; self._workflows[entry_id][i+1].status = "ACTIVE"
        return self._workflows[entry_id][i+1]
    def current_stage(self, entry_id: str) -> str:
        i = self._current.get(entry_id, 0); steps = self._workflows.get(entry_id, [])
        return steps[i].stage if steps and i < len(steps) else "IDEA"
    def skip_step(self, entry_id: str, reason: str) -> WorkflowStep | None: return self.advance(entry_id)
