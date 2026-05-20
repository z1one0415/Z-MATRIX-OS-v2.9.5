from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .d_band_contracts import CANONICAL_COMPONENT_ID, SOURCE_SYSTEM


EXECUTION_RANK = {
    "blocked": 0,
    "none": 0,
    "paper": 1,
    "human_confirm": 2,
    "auto": 3,
}


@dataclass(slots=True)
class ExecutionAggregationResult:
    selected_role: str
    selected_role_execution_mode: str
    final_execution_mode: str
    global_blockers: list[str] = field(default_factory=list)
    reason: str = ""
    selected_candidate: dict[str, Any] | None = None
    component: str = CANONICAL_COMPONENT_ID
    source_system: str = SOURCE_SYSTEM

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _candidate_role(candidate: dict[str, Any]) -> str | None:
    return candidate.get("role") or candidate.get("role_id")


def _candidate_mode(candidate: dict[str, Any]) -> str:
    return (
        candidate.get("execution_mode")
        or candidate.get("execution")
        or candidate.get("mode")
        or "paper"
    )


def aggregate_execution_mode(
    *,
    selected_role: str,
    role_candidates: list[dict[str, Any]],
    global_blockers: list[str] | None = None,
) -> ExecutionAggregationResult:
    """Aggregate execution_mode for B/R/D-Matrix v2.1.

    Rule BRD-EXEC-01:
        final_execution_mode is scoped to selected_role, not min(all roles).

    Rule BRD-EXEC-02:
        D-Band Phase1 paper-only constrains only the dark_horse role. It must not
        automatically suppress B-Matrix or R-Matrix when they are the selected role.

    Rule BRD-EXEC-03:
        Only global_blockers may suppress all roles.
    """
    blockers = list(global_blockers or [])
    selected = next((c for c in role_candidates if _candidate_role(c) == selected_role), None)

    if selected is None:
        return ExecutionAggregationResult(
            selected_role=selected_role,
            selected_role_execution_mode="blocked",
            final_execution_mode="blocked",
            global_blockers=blockers,
            reason="selected_role_not_found",
            selected_candidate=None,
        )

    selected_mode = _candidate_mode(selected)

    if blockers:
        return ExecutionAggregationResult(
            selected_role=selected_role,
            selected_role_execution_mode=selected_mode,
            final_execution_mode="blocked",
            global_blockers=blockers,
            reason="global_blockers_active",
            selected_candidate=selected,
        )

    return ExecutionAggregationResult(
        selected_role=selected_role,
        selected_role_execution_mode=selected_mode,
        final_execution_mode=selected_mode,
        global_blockers=[],
        reason="role_scoped_execution_mode",
        selected_candidate=selected,
    )


def explain_execution_scope(role_candidates: list[dict[str, Any]]) -> list[str]:
    """Return human-readable notes for UI/reporting."""
    notes: list[str] = []
    for candidate in role_candidates:
        role = _candidate_role(candidate) or "unknown"
        matrix = candidate.get("matrix", "unknown")
        mode = _candidate_mode(candidate)
        if matrix in {"D-Band", "D-Matrix", "D-Matrix v2.1"} and mode == "paper":
            notes.append(
                f"{role}/{matrix}: Phase1 paper-only; this does not suppress selected B/R roles unless dark_horse is selected."
            )
    return notes
