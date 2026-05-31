#!/usr/bin/env python3
"""V7-E: V8 entry gate — opens only if all V7 audits pass."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
CASES = W / "runtime_reports" / "cases"

def main():
    labels = json.loads((CASES / "v7_forward_return_labels.json").read_text())
    metrics = json.loads((CASES / "v7_exploratory_factor_metrics.json").read_text())
    adequacy = json.loads((CASES / "v7_sample_adequacy_audit.json").read_text())

    has_labels = labels["label_records"] > 0
    has_metrics = len(metrics["metrics"]) > 0
    alpha_blocked = metrics["alpha_validated"] is False
    t60_insufficient = adequacy["horizon_status"].get("T60") == "INSUFFICIENT"

    ready = has_labels and has_metrics and alpha_blocked

    gate = {
        "status": "V8_EXPANDED_SAMPLE_ENTRY_ALLOWED" if ready else "V8_BLOCKED_INSUFFICIENT_DATA",
        "ready_for_v8_expanded_sample": ready,
        "ready_for_alpha_claim": False,
        "reason": "V7 exploratory complete" + ("; T60 insufficient; V8 required for expanded sample." if t60_insufficient else "."),
        "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    }
    (CASES / "v8_expanded_sample_entry_gate.json").write_text(json.dumps(gate, indent=2, ensure_ascii=False))
    print(f"V8 Gate: {'ALLOWED' if ready else 'BLOCKED'}")

if __name__ == "__main__":
    main()
