from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:16]}"


class ValidationError(ValueError):
    pass


class World(str, Enum):
    TRAINING = "TRAINING_WORLD"
    PAPER = "PAPER_WORLD"
    REAL = "REAL_WORLD"


class ValidationSource(str, Enum):
    HUMAN_MANUAL = "human_manual"
    SYSTEM_DEGRADED = "system_degraded"
    ACTION_PROPOSAL = "action_proposal"
    ALPHA_UNIVERSE = "alpha_universe"
    PAPER_EXECUTION_COACH = "paper_execution_coach"


class PositionStatus(str, Enum):
    PLANNED = "PLANNED"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    RETIRED = "RETIRED"
    DATA_INVALID = "DATA_INVALID"


class DecisionType(str, Enum):
    OPEN = "OPEN"
    ADD = "ADD"
    REDUCE = "REDUCE"
    HOLD = "HOLD"
    CLOSE = "CLOSE"
    CHANGE_HYPOTHESIS = "CHANGE_HYPOTHESIS"
    ANNOTATE = "ANNOTATE"


class CloseReason(str, Enum):
    HYPOTHESIS_CONFIRMED = "hypothesis_confirmed"
    HYPOTHESIS_FAILED = "hypothesis_failed"
    STOP_LOSS = "stop_loss"
    BENCHMARK_UNDERPERFORM = "benchmark_underperform"
    SYSTEM_BLOCKED = "system_blocked"
    HUMAN_CHANGED_MIND = "human_changed_mind"
    EXPIRED = "expired"
    DATA_INVALID = "data_invalid"


class ValidationVerdict(str, Enum):
    PROMOTE_CANDIDATE = "promote_candidate"
    CONTINUE_VALIDATION = "continue_validation"
    RETIRE = "retire"
    ETF_SUBSTITUTE_REVIEW = "etf_substitute_review"
    HUMAN_STRENGTH_SIGNAL = "human_strength_signal"
    HUMAN_BLIND_SPOT_SIGNAL = "human_blind_spot_signal"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class GhostBenchmark:
    benchmark_pair_id: str
    symbol: str
    name: str
    reason: str
    benchmark_type: str = "ETF_OR_INDEX"
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationPlan:
    symbol: str
    name: str
    primary_role: str
    human_hypothesis: str
    ghost_benchmark: GhostBenchmark
    planned_horizon_days: int
    max_acceptable_drawdown: float
    invalidation_conditions: List[str]
    source: str = ValidationSource.HUMAN_MANUAL.value
    validation_id: str = field(default_factory=lambda: new_id("apv"))
    world: str = World.PAPER.value
    role_candidates: List[str] = field(default_factory=list)
    source_proposal_id: Optional[str] = None
    system_verdict_at_entry: str = "INSUFFICIENT_EVIDENCE"
    human_confidence: float = 0.5
    human_reason: str = ""
    evidence_pack_id: Optional[str] = None
    module_versions: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)
    status: str = PositionStatus.PLANNED.value

    def validate(self, require_evidence_pack: bool = False) -> None:
        if self.world != World.PAPER.value:
            raise ValidationError("Alpha validation plan must belong to PAPER_WORLD.")
        if not self.symbol:
            raise ValidationError("symbol is required.")
        if not self.primary_role:
            raise ValidationError("primary_role is required.")
        if not self.human_hypothesis or len(self.human_hypothesis.strip()) < 8:
            raise ValidationError("human_hypothesis is required and must be specific.")
        if not self.ghost_benchmark or not self.ghost_benchmark.symbol:
            raise ValidationError("ghost_benchmark is required.")
        if not self.invalidation_conditions:
            raise ValidationError("invalidation_conditions are required.")
        if self.planned_horizon_days <= 0:
            raise ValidationError("planned_horizon_days must be positive.")
        if self.max_acceptable_drawdown >= 0:
            raise ValidationError("max_acceptable_drawdown must be negative, e.g. -0.07.")
        if require_evidence_pack and not self.evidence_pack_id:
            raise ValidationError("evidence_pack_id is required by policy.")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["ghost_benchmark"] = self.ghost_benchmark.to_dict()
        return d


@dataclass
class AlphaValidationPosition:
    validation_id: str
    symbol: str
    name: str
    primary_role: str
    ghost_benchmark: GhostBenchmark
    entry_price: float
    entry_benchmark_price: float
    quantity: int
    opened_at: str
    planned_horizon_days: int
    max_acceptable_drawdown: float
    human_hypothesis: str
    world: str = World.PAPER.value
    paper_trade_id: str = field(default_factory=lambda: new_id("pt"))
    status: str = PositionStatus.OPEN.value
    cost: float = 0.0
    fees: float = 0.0
    max_adverse_return: float = 0.0
    max_favorable_return: float = 0.0
    last_mark_date: Optional[str] = None
    marks_count: int = 0
    source_proposal_id: Optional[str] = None
    system_verdict_at_entry: str = "INSUFFICIENT_EVIDENCE"
    created_at: str = field(default_factory=utc_now_iso)

    def validate(self) -> None:
        if self.world != World.PAPER.value:
            raise ValidationError("AlphaValidationPosition must be PAPER_WORLD.")
        if self.entry_price <= 0 or self.entry_benchmark_price <= 0:
            raise ValidationError("entry prices must be positive.")
        if self.quantity <= 0:
            raise ValidationError("quantity must be positive.")

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["ghost_benchmark"] = self.ghost_benchmark.to_dict()
        return d


@dataclass
class HumanValidationDecision:
    validation_id: str
    decision_type: str
    system_suggestion: str
    human_decision: str
    reason_code: str
    human_reason: str
    confidence: float
    acknowledged_risks: List[str]
    linked_evidence_ids: List[str] = field(default_factory=list)
    decision_id: str = field(default_factory=lambda: new_id("hvd"))
    decision_time: str = field(default_factory=utc_now_iso)
    world: str = World.PAPER.value

    def validate(self) -> None:
        if self.world != World.PAPER.value:
            raise ValidationError("Human validation decisions must be PAPER_WORLD.")
        if self.decision_type not in {x.value for x in DecisionType}:
            raise ValidationError(f"invalid decision_type: {self.decision_type}")
        if not self.reason_code:
            raise ValidationError("reason_code is required.")
        if not self.human_reason or len(self.human_reason.strip()) < 5:
            raise ValidationError("human_reason is required.")
        if not self.acknowledged_risks:
            raise ValidationError("acknowledged_risks are required.")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MarkToMarketSnapshot:
    validation_id: str
    mark_date: str
    symbol_price: float
    benchmark_price: float
    stock_return: float
    benchmark_return: float
    active_return: float
    max_adverse_return: float
    max_favorable_return: float
    triggered_conditions: List[str] = field(default_factory=list)
    system_verdict: Optional[str] = None
    world: str = World.PAPER.value
    mark_id: str = field(default_factory=lambda: new_id("mtm"))
    created_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SettlementReport:
    validation_id: str
    close_reason: str
    entry_price: float
    exit_price: float
    entry_benchmark_price: float
    exit_benchmark_price: float
    stock_return: float
    benchmark_return: float
    active_return: float
    risk_adjusted_active_return: float
    cost_drag: float
    holding_days: int
    hypothesis_adherence: bool
    rule_changed_midway: bool
    verdict: str
    settlement_id: str = field(default_factory=lambda: new_id("settle"))
    world: str = World.PAPER.value
    settled_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HumanPatternFeature:
    profile_id: str
    window: str
    pattern_type: str
    label: str
    description: str
    sample_count: int
    confidence: str
    supporting_validation_ids: List[str]
    counter_examples: List[str] = field(default_factory=list)
    llm_generated: bool = False
    human_review_status: str = "unreviewed"
    feature_id: str = field(default_factory=lambda: new_id("hpf"))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LLMCoachReport:
    profile_id: str
    period: str
    summary: str
    strengths: List[str]
    blind_spots: List[str]
    system_disagreements: List[str]
    training_suggestions: List[str]
    source_validation_ids: List[str]
    source_report_ids: List[str]
    confidence: str
    report_id: str = field(default_factory=lambda: new_id("coach"))
    generated_at: str = field(default_factory=utc_now_iso)
    permission_scope: str = "LLM_ASSISTS_ONLY"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
