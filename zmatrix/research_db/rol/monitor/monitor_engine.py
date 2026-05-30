"""R2: Monitor Engine — continuous scanning of factor/portfolio/prediction metrics."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class Alert:
    alert_id: str; object_id: str; metric: str; current_value: float; threshold: float
    severity: str = "WARNING"; message: str = ""; timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    acknowledged: bool = False
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class MonitorEngine:
    def __init__(self, threshold_registry=None): self.thresholds = threshold_registry; self._alerts: list[Alert] = []
    def check(self, object_id: str, metrics: dict) -> list[Alert]:
        alerts = []
        if self.thresholds:
            for metric, value in metrics.items():
                t = self.thresholds.get(object_id, metric)
                if t and abs(value) < t.get("min_abs", 0.01): alerts.append(Alert(alert_id=f"A-{object_id}-{metric}", object_id=object_id, metric=metric, current_value=value, threshold=t.get("min_abs", 0.01), severity="WARNING", message=f"{metric} below threshold"))
        self._alerts.extend(alerts); return alerts
    def list_alerts(self) -> list[Alert]: return list(self._alerts)
    def acknowledge(self, alert_id: str):
        for a in self._alerts:
            if a.alert_id == alert_id: a.acknowledged = True
