"""Phase 4-F3: Factor Graveyard — low-IC/low-coverage/high-decay factor retirement."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class GraveyardRecord:
    factor_id: str; factor_name: str; retired_at: str
    retirement_reason: str; tombstone_note: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class FactorGraveyard:
    def __init__(self): self._records: list[GraveyardRecord] = []

    def retire(self, factor_id: str, factor_name: str, reason: str) -> GraveyardRecord:
        r = GraveyardRecord(factor_id=factor_id, factor_name=factor_name,
                           retired_at=datetime.now(timezone.utc).isoformat(), retirement_reason=reason)
        self._records.append(r); return r

    def list_retired(self) -> list[GraveyardRecord]: return list(self._records)
    def is_retired(self, factor_id: str) -> bool:
        return any(r.factor_id == factor_id for r in self._records)
    def count(self) -> int: return len(self._records)

    @staticmethod
    def auto_retire(validation_results: list, graveyard: "FactorGraveyard") -> list[GraveyardRecord]:
        records = []
        for v in validation_results:
            if not v.passed and len(v.fail_reasons) >= 3:
                records.append(graveyard.retire(v.factor_id, v.factor_id, "; ".join(v.fail_reasons)))
        return records
