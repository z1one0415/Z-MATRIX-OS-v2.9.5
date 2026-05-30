"""R2: Alert Engine — threshold breach triggers."""
from __future__ import annotations
from enum import Enum

class AlertSeverity(str, Enum): INFO="INFO"; WARNING="WARNING"; CRITICAL="CRITICAL"

class AlertEngine:
    @staticmethod
    def evaluate(metrics: dict, thresholds: dict) -> list[dict]:
        alerts = []
        for metric, value in metrics.items():
            t = thresholds.get(metric, {})
            if t.get("min") and value < t["min"]: alerts.append({"metric":metric,"value":value,"threshold":t["min"],"severity":AlertSeverity.CRITICAL.value})
            elif t.get("max") and value > t["max"]: alerts.append({"metric":metric,"value":value,"threshold":t["max"],"severity":AlertSeverity.WARNING.value})
        return alerts

    @staticmethod
    def check_drift(drift_magnitude: float, max_drift: float = 0.20) -> list[dict]:
        if drift_magnitude > max_drift: return [{"metric":"drift","value":drift_magnitude,"threshold":max_drift,"severity":"CRITICAL"}]
        return []

    @staticmethod
    def check_prediction_streak(consecutive_failures: int, max_failures: int = 5) -> list[dict]:
        if consecutive_failures >= max_failures: return [{"metric":"prediction_streak","value":consecutive_failures,"threshold":max_failures,"severity":"CRITICAL"}]
        return []
