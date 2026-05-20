from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .contracts import ValidationPlan, World, ValidationError


FORBIDDEN_REAL_ACTIONS = {"BUY", "SELL", "CLEAR", "ADD", "REAL_ORDER", "BROKER_SUBMIT"}


@dataclass
class PolicyDecision:
    allowed: bool
    reasons: List[str] = field(default_factory=list)
    max_action: str = "PAPER_ONLY"


class AlphaValidationPolicyGuard:
    """Hard boundary guard for Z-G16A.

    Alpha Parallel Validation is a PAPER_WORLD validation service. It may create
    paper positions and coach reports, but it must never modify REAL_WORLD ledger
    or produce real broker orders.
    """

    def __init__(self, require_evidence_pack: bool = False):
        self.require_evidence_pack = require_evidence_pack

    def validate_plan_or_raise(self, plan: ValidationPlan) -> None:
        plan.validate(require_evidence_pack=self.require_evidence_pack)
        if plan.world != World.PAPER.value:
            raise ValidationError("Z-G16A can only create PAPER_WORLD plans.")

    def check_requested_action(self, action: str, world: str = World.PAPER.value) -> PolicyDecision:
        if action in FORBIDDEN_REAL_ACTIONS:
            return PolicyDecision(False, [f"forbidden real action: {action}"], max_action="BLOCK")
        if world != World.PAPER.value:
            return PolicyDecision(False, ["Alpha validation only writes PAPER_WORLD."], max_action="BLOCK")
        if action == "PAPER_PROBE":
            return PolicyDecision(True, ["PAPER_PROBE allowed in PAPER_WORLD only."], max_action="PAPER_PROBE")
        if action in {"PAPER_TRACK", "WATCH", "WAIT", "HOLD", "REDUCE", "CLOSE"}:
            return PolicyDecision(True, [], max_action=action)
        return PolicyDecision(True, ["unknown action treated as PAPER_ONLY"], max_action="PAPER_ONLY")
