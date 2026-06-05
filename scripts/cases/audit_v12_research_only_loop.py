#!/usr/bin/env python3
"""V12.0: Research-Only Loop Audit — hardgate scan for forbidden actions and safety violations."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

FORBIDDEN_ACTION_WORDS = [
    "BUY", "SELL", "ADD", "REDUCE", "LONG", "SHORT",
    "POSITION", "ORDER", "TRADE_EXECUTION", "WEIGHT",
    "TARGET_PRICE", "TAKE_PROFIT", "STOP_LOSS",
]


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def scan_forbidden(obj, path: str = "") -> list:
    """Recursively scan for forbidden words in string values."""
    violations = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            current = f"{path}.{k}" if path else k
            if isinstance(v, str):
                for word in FORBIDDEN_ACTION_WORDS:
                    if word in v.upper() or word == v.upper():
                        violations.append(f"FORBIDDEN_WORD {word} in {current}={v}")
            elif isinstance(v, (dict, list)):
                violations.extend(scan_forbidden(v, current))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            current = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                violations.extend(scan_forbidden(item, current))
    return violations


def count_actions(obj: dict, field: str) -> int:
    """Count non-NONE investment/trade actions."""
    count = 0
    for container_key in ["signals", "observations", "autopsy_inputs"]:
        container = obj.get(container_key, obj.get(container_key.rstrip("s"), []))
        if isinstance(container, list):
            for item in container:
                val = item.get(field, "NONE")
                if val != "NONE":
                    count += 1
    # Also check top-level count fields
    if obj.get(f"{field}_count", 0) != 0:
        count = max(count, obj.get(f"{field}_count", 0) if field in ["investment_action_count", "trade_action_count"] else count)
    return count


def main():
    contract = load("v12_research_only_operating_contract.json")
    snapshot = load("v12_research_signal_snapshot.json")
    obs_loop = load("v12_paper_observation_loop.json")
    autopsy = load("v12_z9_research_autopsy_input.json")

    reasons = []

    # Gate check
    gate_status = contract.get("gate_status", "")
    if gate_status != "V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED":
        reasons.append(f"GATE_NOT_ALLOWED: {gate_status}")

    # research_only check
    if not contract.get("research_only", False):
        reasons.append("RESEARCH_ONLY_FALSE")

    # Alpha checks
    for fname, data in [("contract", contract), ("snapshot", snapshot), ("obs_loop", obs_loop), ("autopsy", autopsy)]:
        if data.get("ready_for_alpha_claim", False):
            reasons.append(f"ALPHA_CLAIM_READY_IN_{fname.upper()}")
        if data.get("alpha_validated", False):
            reasons.append(f"ALPHA_VALIDATED_IN_{fname.upper()}")

    # Safety channel checks
    for fname, data in [("contract", contract), ("snapshot", snapshot), ("obs_loop", obs_loop), ("autopsy", autopsy)]:
        for ch in ["production", "broker_runtime", "real_trade"]:
            if data.get(ch) != "BLOCKED":
                reasons.append(f"{ch.upper()}_NOT_BLOCKED_IN_{fname.upper()}")

    # Action count checks
    for fname, data in [("snapshot", snapshot), ("obs_loop", obs_loop), ("autopsy", autopsy)]:
        ia = data.get("investment_action_count", 0)
        ta = data.get("trade_action_count", 0)
        if isinstance(ia, int) and ia != 0:
            reasons.append(f"INVESTMENT_ACTION_COUNT_NONZERO_{fname.upper()}={ia}")
        if isinstance(ta, int) and ta != 0:
            reasons.append(f"TRADE_ACTION_COUNT_NONZERO_{fname.upper()}={ta}")

    # Scan for NONE violations in individual items
    for fname, data, container_key in [
        ("snapshot", snapshot, "signals"),
        ("obs_loop", obs_loop, "observations"),
        ("autopsy", autopsy, "autopsy_inputs"),
    ]:
        container = data.get(container_key, [])
        for item in container:
            if item.get("investment_action", "NONE") != "NONE":
                reasons.append(f"INVESTMENT_ACTION_NOT_NONE_{fname.upper()}")
                break
            if item.get("trade_action", "NONE") != "NONE":
                reasons.append(f"TRADE_ACTION_NOT_NONE_{fname.upper()}")
                break

    # Forbidden word scan
    violations = []
    for fname, data in [("contract", contract), ("snapshot", snapshot), ("obs_loop", obs_loop), ("autopsy", autopsy)]:
        violations.extend(scan_forbidden(data, fname))

    if violations:
        reasons.append(f"FORBIDDEN_ACTION_VIOLATIONS:{len(violations)}")

    blocked = len(reasons) > 0

    result = {
        "status": "V12_RESEARCH_ONLY_LOOP_AUDIT_PASS" if not blocked else "V12_RESEARCH_ONLY_LOOP_AUDIT_BLOCKED",
        "research_only_loop_confirmed": not blocked,
        "forbidden_action_violations": violations + reasons,
        "blocking_reasons": reasons,
        "investment_action_count": 0,
        "trade_action_count": 0,
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(result, open(C / "v12_research_only_loop_audit.json", "w"), indent=2)
    print(f"V12.0 Audit: {result['status']} | violations={len(violations)+len(reasons)}")


if __name__ == "__main__":
    main()
