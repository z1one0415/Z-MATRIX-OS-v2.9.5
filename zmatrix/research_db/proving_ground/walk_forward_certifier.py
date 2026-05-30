"""F.5-5: Walk Forward Certification — PASS/CONDITIONAL/FAIL with full metrics."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class CertificationResult:
    factor_id: str; status: str = "FAIL"
    train_ic: float = 0.0; val_ic: float = 0.0; forward_ic: float = 0.0
    ic_decay: float = 0.0; overfit_score: float = 0.0
    stability_score: float = 0.0; cert_grade: str = "F"
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class WalkForwardCertifier:
    @staticmethod
    def certify(factor_id: str, train_data: list[dict], val_data: list[dict], forward_data: list[dict]) -> CertificationResult:
        def _mean_ic(d): ics=[x.get("ic",0) for x in d if x.get("ic") is not None]; return sum(ics)/len(ics) if ics else 0.0
        r = CertificationResult(factor_id=factor_id)
        r.train_ic = _mean_ic(train_data); r.val_ic = _mean_ic(val_data); r.forward_ic = _mean_ic(forward_data)
        r.ic_decay = abs(r.train_ic - r.forward_ic)
        r.overfit_score = abs(r.train_ic - r.val_ic) / max(abs(r.train_ic), 0.01)
        import statistics
        all_ic = [_mean_ic(d) for d in [train_data, val_data, forward_data] if d]
        r.stability_score = 1.0 - (statistics.stdev(all_ic) / max(abs(statistics.mean(all_ic)), 0.01)) if len(all_ic)>1 else 0.0
        score = (1.0 - r.overfit_score) * 0.4 + r.stability_score * 0.3 + (1.0 if abs(r.forward_ic)>0.02 else 0.0) * 0.3
        if score > 0.7: r.status = "PASS"; r.cert_grade = "A"
        elif score > 0.5: r.status = "CONDITIONAL"; r.cert_grade = "B"
        elif score > 0.3: r.status = "CONDITIONAL"; r.cert_grade = "C"
        else: r.status = "FAIL"; r.cert_grade = "F"
        return r
