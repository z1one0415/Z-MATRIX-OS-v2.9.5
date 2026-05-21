"""Event store with INV-TG18-04 Auto-Weight Freeze

No auto-adjust without ≥50 strict T+N resolved samples.
CURRENT_PRICE_PROXY samples never trigger auto-adjust.
"""
from __future__ import annotations
import json, os
from datetime import datetime
from pathlib import Path


class ConfigurationLockedError(Exception):
    """Raised when auto-adjust attempted without meeting minimum requirements."""
    pass


class PredictionEventStore:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or str(
            Path(__file__).resolve().parents[2] / "hermes" / "calibration_db.json"
        )
        self.min_strict_samples = 50

    def _load_db(self) -> dict:
        if os.path.exists(self.db_path):
            with open(self.db_path) as f:
                return json.load(f)
        return {"predictions": [], "calibration_log": [], "resolved_samples": []}

    def _save_db(self, db: dict):
        with open(self.db_path, "w") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)

    def count_resolved_strict(self) -> int:
        """Count resolved samples that were strict T+N (not CURRENT_PRICE_PROXY)."""
        db = self._load_db()
        return sum(
            1 for s in db.get("resolved_samples", [])
            if s.get("is_strict_t_plus_n") and s.get("resolved")
        )

    def is_auto_adjust_allowed(self) -> tuple[bool, str]:
        """INV-TG18-04: check if auto-adjust is permitted."""
        strict_count = self.count_resolved_strict()
        if strict_count < self.min_strict_samples:
            return False, f"Only {strict_count}/{self.min_strict_samples} strict T+N samples"
        return True, f"{strict_count} strict samples, auto-adjust allowed"

    def assert_auto_adjust_safe(self):
        """Invariant guard — raises ConfigurationLockedError if not met."""
        allowed, reason = self.is_auto_adjust_allowed()
        if not allowed:
            raise ConfigurationLockedError(
                f"Auto-weight adjustment locked: {reason}. "
                f"CURRENT_PRICE_PROXY samples do not count toward minimum."
            )

    def can_auto_adjust(self) -> bool:
        return self.count_resolved_strict() >= self.min_strict_samples
