from __future__ import annotations

from typing import Any, Dict, List

from .contracts import ValidationPlan
from .ghost_benchmark import BenchmarkBindingRequest, GhostBenchmarkBinder
from .policy import AlphaValidationPolicyGuard


class ValidationPlanBuilder:
    def __init__(self, benchmark_binder: GhostBenchmarkBinder | None = None, policy: AlphaValidationPolicyGuard | None = None):
        self.binder = benchmark_binder or GhostBenchmarkBinder()
        self.policy = policy or AlphaValidationPolicyGuard()

    def from_payload(self, payload: Dict[str, Any]) -> ValidationPlan:
        primary_role = payload.get("primary_role") or payload.get("role") or "R_MATRIX"
        ghost_benchmark = self.binder.bind(
            BenchmarkBindingRequest(
                primary_role=primary_role,
                explicit_symbol=payload.get("ghost_benchmark_symbol"),
                explicit_name=payload.get("ghost_benchmark_name"),
                reason=payload.get("ghost_benchmark_reason"),
                sector=payload.get("sector"),
                chain=payload.get("chain"),
            )
        )
        invalidation: List[str] = payload.get("invalidation_conditions") or []
        if isinstance(invalidation, str):
            invalidation = [invalidation]
        plan = ValidationPlan(
            symbol=payload["symbol"],
            name=payload.get("name") or payload["symbol"],
            primary_role=primary_role,
            role_candidates=payload.get("role_candidates") or [primary_role],
            human_hypothesis=payload.get("human_hypothesis") or payload.get("hypothesis") or "",
            ghost_benchmark=ghost_benchmark,
            planned_horizon_days=int(payload.get("planned_horizon_days", 20)),
            max_acceptable_drawdown=float(payload.get("max_acceptable_drawdown", -0.07)),
            invalidation_conditions=invalidation,
            source=payload.get("source", "human_manual"),
            source_proposal_id=payload.get("source_proposal_id"),
            system_verdict_at_entry=payload.get("system_verdict_at_entry", "INSUFFICIENT_EVIDENCE"),
            human_confidence=float(payload.get("human_confidence", 0.5)),
            human_reason=payload.get("human_reason", ""),
            evidence_pack_id=payload.get("evidence_pack_id"),
            module_versions=payload.get("module_versions") or {},
        )
        self.policy.validate_plan_or_raise(plan)
        return plan
