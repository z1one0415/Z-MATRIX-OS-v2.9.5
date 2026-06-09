"""☯️ Degraded Contract — explicit degradation protocol for G-Core modules.

When a dependency is unavailable, modules MUST return a DegradedContract
instead of pass/stub/placeholder. This ensures:
1. System knows capability is degraded (not silently passing)
2. Downstream consumers get explicit data_gap signals
3. Skeleton guard can distinguish legal degradation from dead code
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class DegradedContract:
    status: str
    capability_available: bool
    reason: str
    fallback_mode: str
    source: str
    next_required_action: str
    data_gap: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["is_stub"] = False
        payload["is_placeholder"] = False
        return payload


def dependency_unavailable(source: str, reason: str, next_action: str = "RESTORE_DEPENDENCY") -> Dict[str, Any]:
    """Standard degraded response when a dependency is unavailable."""
    return DegradedContract(
        status="DEGRADED_DEPENDENCY_UNAVAILABLE",
        capability_available=False,
        reason=reason,
        fallback_mode="SAFE_NOOP_WITH_EXPLICIT_DATA_GAP",
        source=source,
        next_required_action=next_action,
        data_gap={"dependency_missing": True},
    ).to_dict()


def risk_data_degraded(source: str, reason: str) -> Dict[str, Any]:
    """G17 fail-safe: missing risk data -> ORANGE / must_review."""
    return {
        "status": "RISK_DATA_DEGRADED",
        "capability_available": False,
        "risk_level": "ORANGE",
        "add_position_allowed": False,
        "paper_track_allowed": False,
        "must_review": True,
        "reason": reason,
        "source": source,
        "fallback_mode": "FAIL_SAFE_REVIEW_REQUIRED",
        "next_required_action": "RESTORE_RISK_DATA_SOURCE",
        "is_stub": False,
        "is_placeholder": False,
    }


def data_gap_recorded(module: str, missing_inputs: list) -> Dict[str, Any]:
    """G05 fail-safe: missing data -> still write memory with gap noted."""
    return {
        "status": "DATA_GAP_RECORDED",
        "capability_available": True,
        "module": module,
        "data_gap": {"missing_inputs": missing_inputs},
        "memory_written": True,
        "next_required_action": "FILL_MISSING_INPUTS_NEXT_RUN",
        "is_stub": False,
        "is_placeholder": False,
    }


def chain_evidence_insufficient(missing: list) -> Dict[str, Any]:
    """G15 fail-safe: missing chain data -> low-confidence evidence report."""
    return {
        "status": "CHAIN_EVIDENCE_INSUFFICIENT",
        "capability_available": True,
        "evidence_layers": {
            "L1_hard_data": [],
            "L2_company_disclosure": [],
            "L3_cross_validation": [],
            "L4_industry_opinion": [],
            "L5_narrative": [],
        },
        "research_confidence": "LOW",
        "data_gap": {"missing_chain_map": True, "missing_items": missing},
        "next_required_action": "IMPORT_CHAIN_MAP_OR_MANUAL_EVIDENCE",
        "is_stub": False,
        "is_placeholder": False,
    }
