# allowlist: forbidden-token-definition
"""Expert Domain Contract — reviewer output, validation, aggregation"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from collections import Counter


class ReviewVerdict(str, Enum):
    PASS = "PASS"
    WATCH = "WATCH"
    BLOCK = "BLOCK"
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"
    CONFLICTED = "CONFLICTED"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


_VALID_VERDICTS = frozenset(v.value for v in ReviewVerdict)
_FORBIDDEN_TOKENS = frozenset({"BUY", "SELL", "AUTO_EXECUTE"})


def _contains_forbidden_token(data: dict) -> bool:
    def _recurse(obj):
        if isinstance(obj, str):
            upper = obj.upper()
            for tok in _FORBIDDEN_TOKENS:
                if tok in upper:
                    return True
        elif isinstance(obj, dict):
            for v in obj.values():
                if _recurse(v):
                    return True
        elif isinstance(obj, list):
            for v in obj:
                if _recurse(v):
                    return True
        return False
    return _recurse(data)


@dataclass
class ReviewerSkillOutput:
    reviewer_id: str
    target_ref: str
    verdict: str
    confidence: float
    risk_flags: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    reason_short: str = ""
    production_allowed: bool = False


def create_review_output(
    reviewer_id: str,
    target_ref: str,
    verdict: str,
    confidence: float,
    reason_short: str,
) -> dict:
    return {
        "reviewer_id": reviewer_id,
        "target_ref": target_ref,
        "verdict": verdict,
        "confidence": confidence,
        "risk_flags": [],
        "missing_evidence": [],
        "reason_short": reason_short,
        "production_allowed": False,
    }


def validate_review_output(output: dict) -> dict:
    errors: list[str] = []

    if _contains_forbidden_token(output):
        errors.append("Output contains forbidden token (BUY/SELL/AUTO_EXECUTE)")

    verdict = output.get("verdict")
    if verdict not in _VALID_VERDICTS:
        errors.append(f"Invalid verdict '{verdict}': must be one of {sorted(_VALID_VERDICTS)}")

    confidence = output.get("confidence", 0.0)
    if not isinstance(confidence, (int, float)) or confidence < 0.0 or confidence > 1.0:
        errors.append(f"confidence must be 0.0-1.0, got {confidence}")

    if output.get("production_allowed") is True:
        errors.append("production_allowed must be false")

    return {"valid": len(errors) == 0, "errors": errors}


def aggregate_review_results(review_outputs: list[dict]) -> dict:
    if not review_outputs:
        return {
            "consensus_verdict": "DATA_INSUFFICIENT",
            "pass_count": 0,
            "block_count": 0,
            "conflicts": [],
        }

    verdicts = [r.get("verdict") for r in review_outputs]
    pass_count = sum(1 for v in verdicts if v == "PASS")
    block_count = sum(1 for v in verdicts if v == "BLOCK")

    conflicts: list[dict] = []
    for i in range(len(review_outputs)):
        for j in range(i + 1, len(review_outputs)):
            v_i = verdicts[i]
            v_j = verdicts[j]
            if v_i != v_j:
                conflicts.append({
                    "reviewer_a": review_outputs[i]["reviewer_id"],
                    "reviewer_b": review_outputs[j]["reviewer_id"],
                    "verdict_a": v_i,
                    "verdict_b": v_j,
                })

    counter = Counter(verdicts)
    most_common = counter.most_common()

    if len(most_common) == 1 or (len(most_common) > 1 and most_common[0][1] > most_common[1][1]):
        consensus_verdict = most_common[0][0]
    elif block_count > 0:
        consensus_verdict = "BLOCK"
    else:
        consensus_verdict = "CONFLICTED"

    return {
        "consensus_verdict": consensus_verdict,
        "pass_count": pass_count,
        "block_count": block_count,
        "conflicts": conflicts,
    }
