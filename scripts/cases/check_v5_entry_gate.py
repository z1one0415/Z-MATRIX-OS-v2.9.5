#!/usr/bin/env python3
"""Check if V5 (Real Return / Benchmark Alpha) entry gate is open."""
import json
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
READINESS = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_market_data_readiness.json"
RETURN = WORKSPACE / "runtime_reports" / "cases" / "core_12_real_return_readiness.json"

def main():
    rd = json.loads(READINESS.read_text()) if READINESS.exists() else {"summary": {}}
    rr = json.loads(RETURN.read_text()) if RETURN.exists() else {"summary": {}}

    gates = {
        "daily_price_real_read_only": rd["summary"].get("daily_price_real", 0),
        "adjustment_factor_ready": 0,
        "benchmark_real_read_only": False,
        "calendar_real_read_only": False,
        "ready_for_real_return": rr["summary"].get("ready_for_real_return", 0),
        "ready_for_alpha_claim": 0,
    }

    all_real_data = gates["daily_price_real_read_only"] >= 12
    ready = all_real_data

    gate = {
        "status": "V5_ENTRY_ALLOWED" if ready else "V5_ENTRY_BLOCKED_WAITING_USER_MARKET_DATA",
        **gates,
        "v5_entry_allowed": ready,
        "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED",
    }
    (WORKSPACE / "runtime_reports" / "cases" / "v5_entry_gate.json").write_text(json.dumps(gate, indent=2, ensure_ascii=False))
    print("V5 Entry Gate: " + ("ALLOWED" if ready else "BLOCKED") + " | Price REAL: " + str(gates["daily_price_real_read_only"]) + "/12")

if __name__ == "__main__":
    main()
