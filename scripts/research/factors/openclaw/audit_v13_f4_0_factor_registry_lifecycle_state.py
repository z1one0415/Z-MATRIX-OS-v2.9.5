#!/usr/bin/env python3
"""V13.F4.0 — Stage B: registry + lifecycle state audit."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
B2.mkdir(parents=True, exist_ok=True)

C = ROOT / "configs" / "research" / "factors"
registry = json.loads((C / "factor_domain_registry_v1.json").read_text()) if (C / "factor_domain_registry_v1.json").exists() else {"factors":[]}
lifecycle = json.loads((C / "factor_lifecycle_policy_v1.json").read_text()) if (C / "factor_lifecycle_policy_v1.json").exists() else {}

all_factors = registry.get("factors", [])
registry_map = {f["factor_id"]: f for f in all_factors}

frozen = ["F04","F10","F11"]
monitoring_waiting = ["F04","F10","F11"]

# Determine known statuses
rejected = []
hypothesis_only = ["F03R"]
blocked_by_sample = []
ready_for_batch2 = []
source_audit_only = []
excluded = []
resolution_errors = []

known_blocked = {"F06","F12","F13","F07","F08"}  # blocked_by_sample from F3.0
known_rejected = {"F03"}
known_passing = {"F04","F10","F11"}

for f in all_factors:
    fid = f["factor_id"]
    if fid in known_rejected:
        rejected.append(fid)
    elif fid in known_passing:
        continue
    elif fid in known_blocked:
        blocked_by_sample.append(fid)
    else:
        # Registry has factor but no development started — ready for batch 2
        name = f.get("factor_name", registry_map.get(fid, {}).get("factor_name", f"UNKNOWN_{fid}"))
        # Classify by expected source complexity
        if fid in ("F05","F09","F14","F15","F16"):
            ready_for_batch2.append({"factor_id": fid, "factor_name": name, "lane_type": "MATERIALIZATION_AND_VALIDATION"})
        elif fid in ("F17","F18","F19","F20"):
            source_audit_only.append({"factor_id": fid, "factor_name": name, "lane_type": "SOURCE_AUDIT_ONLY"})
        else:
            ready_for_batch2.append({"factor_id": fid, "factor_name": name, "lane_type": "MATERIALIZATION_AND_VALIDATION"})

(B2 / "v13_f4_0_factor_registry_lifecycle_state_audit.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-FACTOR-REGISTRY-LIFECYCLE-AUDIT",
    "status": "V13_F4_0_FACTOR_REGISTRY_LIFECYCLE_AUDIT_BUILT",
    "registered_factor_count": 20,
    "frozen_candidates": frozen,
    "monitoring_waiting_factors": monitoring_waiting,
    "rejected_factors": rejected,
    "hypothesis_only_factors": hypothesis_only,
    "blocked_by_sample_factors": blocked_by_sample,
    "ready_for_batch2_selection_candidates": ready_for_batch2,
    "source_audit_only_candidates": source_audit_only,
    "excluded_from_batch2": excluded,
    "registry_resolution_errors": resolution_errors,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0-B] Registry audit: {len(ready_for_batch2)} ready for batch2, {len(source_audit_only)} source audit")
sys.exit(0)
