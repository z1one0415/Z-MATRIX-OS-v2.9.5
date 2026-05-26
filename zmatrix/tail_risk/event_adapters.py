"""Tail-Risk Event Adapters — build RiskEvent (no auto-append)"""
from __future__ import annotations

from zmatrix.event_store.builders import build_event


def build_tail_risk_event(tail_risk_controller_preview: dict) -> dict:
    payload = {
        "event_subtype": "TailRiskController",
        "controller_id": tail_risk_controller_preview.get("controller_id", ""),
        "final_state": tail_risk_controller_preview.get("final_state", ""),
        "final_decision": tail_risk_controller_preview.get("final_decision", ""),
        "requires_human_review": tail_risk_controller_preview.get("action_policy_preview", {}).get("requires_human_review", True),
    }
    return build_event(
        event_type="RiskEvent",
        producer_module="zmatrix.tail_risk.event_adapters.build_tail_risk_event",
        payload=payload,
    )


def build_tail_gate_event(gate_result: dict) -> dict:
    payload = {
        "event_subtype": "TailRiskGate",
        "gate_id": gate_result.get("gate_id", ""),
        "gate_type": gate_result.get("gate_type", ""),
        "state": gate_result.get("state", ""),
        "decision": gate_result.get("decision", ""),
        "action_downgrade": gate_result.get("action_downgrade", ""),
    }
    return build_event(
        event_type="RiskEvent",
        producer_module="zmatrix.tail_risk.event_adapters.build_tail_gate_event",
        payload=payload,
    )


def build_risk_isolation_event(risk_isolation_preview: dict) -> dict:
    payload = {
        "event_subtype": "RiskIsolationPreview",
        "isolation_id": risk_isolation_preview.get("isolation_id", ""),
        "ticker": risk_isolation_preview.get("ticker", ""),
        "isolation_reason": risk_isolation_preview.get("isolation_reason", ""),
        "requires_human_review": risk_isolation_preview.get("requires_human_review", True),
    }
    return build_event(
        event_type="RiskEvent",
        producer_module="zmatrix.tail_risk.event_adapters.build_risk_isolation_event",
        payload=payload,
    )
