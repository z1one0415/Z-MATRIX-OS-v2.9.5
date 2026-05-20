from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any


CANONICAL_PRODUCT_NAME = "D-Matrix"
CANONICAL_VERSION = "v2.1"
CANONICAL_COMPONENT_ID = "D-Matrix v2.1"
SOURCE_SYSTEM = "Z-MATRIX OS v2.9"
DBAND_MODULE_NAME = "D-Band v2.1-lite"
DBAND_PHASE = "Phase1"


class DBandStage(str, Enum):
    COLD_IDLE = "D0_COLD_IDLE"
    THEME_SEED = "D1_THEME_SEED"
    PREHEAT = "D2_PREHEAT"
    D3_CANDIDATE = "D3_CANDIDATE"
    IGNITION_READY = "D3_IGNITION_READY"  # Phase2 only
    BREAKOUT = "D4_BREAKOUT"
    MANIA = "D5_MANIA"
    EXHAUSTION = "D6_EXHAUSTION"


STAGE_RANK = {
    DBandStage.COLD_IDLE: 0,
    DBandStage.THEME_SEED: 1,
    DBandStage.PREHEAT: 2,
    DBandStage.D3_CANDIDATE: 3,
    DBandStage.IGNITION_READY: 4,
    DBandStage.BREAKOUT: 5,
    DBandStage.MANIA: 6,
    DBandStage.EXHAUSTION: 7,
}


class ExecutionMode(str, Enum):
    BLOCKED = "blocked"
    NONE = "none"
    PAPER = "paper"
    HUMAN_CONFIRM = "human_confirm"
    AUTO = "auto"  # forbidden in Phase1


class AllowedAction(str, Enum):
    NONE = "NONE"
    WATCH = "WATCH"
    PREHEAT_POOL = "PREHEAT_POOL"
    PAPER_PROBE_PLAN = "PAPER_PROBE_PLAN"
    HUMAN_CONFIRM_PROBE = "HUMAN_CONFIRM_PROBE"  # Phase2+
    HUMAN_CONFIRM_ENTRY = "HUMAN_CONFIRM_ENTRY"  # D4+
    REDUCE = "REDUCE"
    EXIT = "EXIT"


@dataclass(slots=True)
class DataCompleteness:
    blackhorse_gene: bool = False
    sector_ignition: bool = False
    vol_price_preload: bool = False
    theme_seed: bool = False
    smart_money: bool = False
    micro_absorption: bool = False

    def independent_signal_count(self) -> int:
        return sum(
            bool(v)
            for v in [
                self.blackhorse_gene,
                self.sector_ignition,
                self.vol_price_preload,
                self.theme_seed,
                self.smart_money,
                self.micro_absorption,
            ]
        )

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(slots=True)
class ScoreBreakdown:
    blackhorse_gene: float | None = None
    sector_ignition: float | None = None
    vol_price_preload: float | None = None
    theme_mapping: float | None = None
    raw_score: float | None = None
    final_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class DBandReport:
    code: str
    name: str
    timestamp: str
    d_lifecycle_stage: DBandStage
    d_stage_variant: str
    d_early_score: float
    d_early_score_ceiling: float
    d_confirm_score: float | None
    execution_mode: ExecutionMode
    allowed_action: AllowedAction
    real_trade_allowed: bool
    data_completeness: DataCompleteness
    score_breakdown: ScoreBreakdown
    theme_seed: str | None = None
    theme_unverified: bool = True
    sector_ignition: bool = False
    next_triggers: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    caps_applied: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def validate_phase1(self) -> None:
        """Phase1 hard contract: early != confirmed; paper != real trade."""
        if self.real_trade_allowed:
            raise ValueError("Phase1 D-Band must not allow real trade")
        if self.execution_mode not in {ExecutionMode.NONE, ExecutionMode.PAPER}:
            raise ValueError("Phase1 execution_mode must be none/paper")
        if self.allowed_action in {
            AllowedAction.HUMAN_CONFIRM_PROBE,
            AllowedAction.HUMAN_CONFIRM_ENTRY,
            AllowedAction.REDUCE,
            AllowedAction.EXIT,
        }:
            raise ValueError("Phase1 D-Band must not emit executable trading action")
        if STAGE_RANK[self.d_lifecycle_stage] > STAGE_RANK[DBandStage.D3_CANDIDATE]:
            raise ValueError("Phase1 lifecycle cannot exceed D3_CANDIDATE")

    def to_dict(self) -> dict[str, Any]:
        self.validate_phase1()
        return {
            "code": self.code,
            "name": self.name,
            "timestamp": self.timestamp,
            "d_lifecycle_stage": self.d_lifecycle_stage.value,
            "d_stage_variant": self.d_stage_variant,
            "d_early_score": self.d_early_score,
            "d_early_score_ceiling": self.d_early_score_ceiling,
            "d_confirm_score": self.d_confirm_score,
            "execution_mode": self.execution_mode.value,
            "allowed_action": self.allowed_action.value,
            "real_trade_allowed": self.real_trade_allowed,
            "data_completeness": self.data_completeness.to_dict(),
            "score_breakdown": self.score_breakdown.to_dict(),
            "theme_seed": self.theme_seed,
            "theme_unverified": self.theme_unverified,
            "sector_ignition": self.sector_ignition,
            "next_triggers": self.next_triggers,
            "forbidden": self.forbidden,
            "caps_applied": self.caps_applied,
            "warnings": self.warnings,
        }

    def to_role_candidate(self) -> dict[str, Any]:
        d = self.to_dict()
        return {
            "role": "dark_horse",
            "matrix": "D-Band",
            "component": CANONICAL_COMPONENT_ID,
            "source_system": SOURCE_SYSTEM,
            "stage": d["d_lifecycle_stage"],
            "early_score": d["d_early_score"],
            "execution_mode": d["execution_mode"],
            "execution": d["execution_mode"],  # backward-compatible alias
            "allowed_action": d["allowed_action"],
            "real_trade_allowed": False,
            "note": "D-Band Phase1 paper-only; does not suppress selected B/R role",
        }
