#!/usr/bin/env python3
"""V10-A: Build council input pack from full V9 evidence chain."""
import json
from pathlib import Path
W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

def main():
    sel = json.loads((C / "v9_factor_selection_gate.json").read_text())
    stab = json.loads((C / "v9_formal_factor_stability.json").read_text())
    decay = json.loads((C / "v9_factor_decay_analysis.json").read_text())
    rob = json.loads((C / "v9_factor_robustness.json").read_text())
    
    prom = [r for r in sel["selection_results"] if r["decision"] == "PROMOTE_TO_COUNCIL_REVIEW"]
    watch = [r for r in sel["selection_results"] if r["decision"] == "WATCH"]
    rej = [r for r in sel["selection_results"] if "REJECT" in r.get("decision", "")]
    
    pfs = []
    for p in prom:
        fid, h = p["factor_id"], p["horizon"]
        sm = next((m for m in stab["metrics"] if m["factor_id"] == fid and m["horizon"] == h), {})
        dm = next((d for d in decay["decay_results"] if d["factor_id"] == fid), {})
        rm = next((r for r in rob["robustness_results"] if r["factor_id"] == fid), {})
        pfs.append({
            "factor_id": fid, "horizon": h,
            "mean_rankic": sm.get("mean_rankic"),
            "rankic_ir": sm.get("rankic_ir"),
            "valid_date_count": sm.get("valid_date_count"),
            "positive_rankic_ratio": sm.get("positive_rankic_ratio"),
            "decay_pattern": dm.get("decay_pattern"),
            "decay_consistent": dm.get("decay_consistent", False),
            "robustness_grade": rm.get("robustness_grade"),
            "ready_for_alpha_claim": False, "alpha_validated": False,
        })
    
    inp = {
        "status": "V10_COUNCIL_INPUT_PACK_BUILT",
        "promoted_factor_count": len(prom),
        "watch_factor_count": len(watch),
        "rejected_factor_count": len(rej),
        "review_input_count": len(pfs),
        "input_limitations": [
            "V9 robustness uses T20 horizon as primary proxy.",
            "No financial/valuation/fundamental factors.",
            "No transaction cost/slippage/liquidity model.",
            "No market-cap neutralization.",
            "Not an investment verdict.",
        ],
        "promoted_factors": pfs,
        "ready_for_council_research_review": len(pfs) >= 1,
        "ready_for_alpha_claim": False, "alpha_validated": False,
    }
    (C / "v10_council_input_pack.json").write_text(json.dumps(inp, indent=2, ensure_ascii=False))
    null_ev = sum(1 for pf in pfs if pf.get("mean_rankic") is None)
    print(f"Input pack: {len(pfs)} promoted, {len(watch)} watch, {len(rej)} rejected, null_evidence={null_ev}")

if __name__ == "__main__":
    main()
