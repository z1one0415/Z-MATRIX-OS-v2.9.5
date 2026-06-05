#!/usr/bin/env python3
"""V12.0: Build Research-Only Operating Contract — scope lock + action boundary."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"


def load(name: str) -> dict:
    p = C / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    gate = load("v12_alpha_operating_loop_entry_gate.json")
    gate_status = gate.get("status", "UNKNOWN")

    allowed = gate_status == "V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED"

    ct = {
        "status": (
            "V12_RESEARCH_ONLY_OPERATING_CONTRACT_BUILT"
            if allowed
            else "V12_RESEARCH_ONLY_OPERATING_CONTRACT_BLOCKED"
        ),
        "gate_status": gate_status,
        "research_only": allowed,
        "operating_mode": "RESEARCH_ONLY_PAPER_LOOP" if allowed else "BLOCKED",
        "allowed_actions": [
            "BUILD_RESEARCH_SIGNAL",
            "RUN_PAPER_OBSERVATION",
            "WRITE_Z9_AUTOPSY_INPUT",
            "UPDATE_FACTOR_LIFECYCLE_RESEARCH_STATE",
            "GENERATE_RESEARCH_REPORT",
        ] if allowed else [],
        "forbidden_actions": [
            "BUY", "SELL", "ADD_POSITION", "REDUCE_POSITION",
            "BROKER_ORDER", "REAL_TRADE", "PRODUCTION_SIGNAL",
            "ALPHA_VALIDATED_CLAIM",
        ],
        "ready_for_alpha_claim": False,
        "alpha_validated": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
    }

    json.dump(ct, open(C / "v12_research_only_operating_contract.json", "w"), indent=2)
    print(f"V12.0 Contract: {ct['status']} | research_only={ct['research_only']}")


if __name__ == "__main__":
    main()
