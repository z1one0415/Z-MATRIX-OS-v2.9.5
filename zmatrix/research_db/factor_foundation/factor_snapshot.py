"""Batch-B: Factor Snapshot + Audit + Registry."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class FactorSnapshot:
    factor_id: str; factor_name: str; computed_at: str = ""
    ic: float = 0.0; rankic: float = 0.0; hit_rate: float = 0.0
    win_rate: float = 0.0; long_short_spread: float = 0.0
    turnover: float = 0.0; coverage: float = 0.0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

@dataclass
class FactorAudit:
    audit_id: str; factor_id: str; checks_passed: int = 0
    checks_failed: int = 0; auditor_notes: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorRegistryAdapter:
    def __init__(self): self._factors: dict[str, dict] = {}
    def register_factor(self, factor_id: str, factor_info: dict): self._factors[factor_id] = factor_info
    def get_factor(self, factor_id: str) -> dict | None: return self._factors.get(factor_id)
    def list_factors(self) -> list[dict]: return list(self._factors.values())
    def count(self) -> int: return len(self._factors)

def build_snapshot(factor_id: str, metrics) -> FactorSnapshot:
    return FactorSnapshot(factor_id=factor_id, factor_name=getattr(metrics,'factor_name',''),
        ic=getattr(metrics,'ic',0), rankic=getattr(metrics,'rankic',0),
        hit_rate=getattr(metrics,'hit_rate',0), win_rate=getattr(metrics,'win_rate',0),
        coverage=getattr(metrics,'coverage',0))

def audit_snapshot(snapshot: FactorSnapshot, thresholds: dict) -> FactorAudit:
    checks = {"ic_min": snapshot.ic >= thresholds.get("ic_min", 0.02),
              "rankic_min": snapshot.rankic >= thresholds.get("rankic_min", 0.02),
              "coverage_min": snapshot.coverage >= thresholds.get("coverage_min", 0.5)}
    passed = sum(1 for v in checks.values() if v)
    return FactorAudit(audit_id=f"AUDIT-{snapshot.factor_id}", factor_id=snapshot.factor_id,
                       checks_passed=passed, checks_failed=len(checks)-passed)
