"""Phase 4-F2: Factor Validator — IC/RankIC/Stability/Decay/Turnover/Coverage validation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ValidationResult:
    factor_id: str; passed: bool = False
    ic: float = 0.0; rankic: float = 0.0; stability: float = 0.0
    decay: float = 0.0; turnover: float = 0.0; coverage: float = 0.0
    fail_reasons: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorValidator:
    DEFAULT_THRESHOLDS = {"ic_min": 0.02, "rankic_min": 0.02, "coverage_min": 0.3, "stability_max": 2.0, "decay_max": 0.05}

    @staticmethod
    def validate(factor_id: str, metrics: dict, thresholds: dict | None = None) -> ValidationResult:
        t = thresholds or FactorValidator.DEFAULT_THRESHOLDS
        r = ValidationResult(factor_id=factor_id)
        r.ic = metrics.get("ic", 0); r.rankic = metrics.get("rankic", 0)
        r.stability = metrics.get("stability", 0); r.decay = metrics.get("decay", 0)
        r.turnover = metrics.get("turnover", 0); r.coverage = metrics.get("coverage", 0)
        fails = []
        if abs(r.ic) < t["ic_min"]: fails.append(f"IC {r.ic}<{t['ic_min']}")
        if abs(r.rankic) < t["rankic_min"]: fails.append(f"RankIC {r.rankic}<{t['rankic_min']}")
        if r.coverage < t["coverage_min"]: fails.append(f"Coverage {r.coverage}<{t['coverage_min']}")
        if r.stability > t["stability_max"]: fails.append(f"Stability {r.stability}>{t['stability_max']}")
        if abs(r.decay) > t["decay_max"]: fails.append(f"Decay {abs(r.decay)}>{t['decay_max']}")
        r.fail_reasons = fails; r.passed = len(fails) == 0
        return r

    @staticmethod
    def batch_validate(factors: list[dict]) -> list[ValidationResult]:
        return [FactorValidator.validate(f["factor_id"], f.get("metrics", {})) for f in factors]
