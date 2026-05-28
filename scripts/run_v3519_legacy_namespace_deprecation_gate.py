#!/usr/bin/env python3
"""v3.5.19 Legacy Namespace Deprecation Gate"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from collections import Counter

LEGACY = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","WATCH_ONLY"]
CANONICAL = ["ROLE_CORE","ROLE_ROT","ROLE_HUNT","ROLE_WATCH","ROLE_BLOCK"]
ALLOW_KEYWORDS = ["account_constitution.py","pre_trade_checklist.py","z8_position_control.py","investment_role_workflow.py","brd_result_audit","legacy_migration_plan","adapter_first_integration","classifier_v2_replay","role_replay","role_taxonomy_closeout","legacy_namespace_deprecation","tests","run_v35","run_v351","scripts","discover_brd","zmatrix/"]
BLOCK_KEYWORDS = ["classifier_v2_replay","adapter_first_integration","role_taxonomy_closeout","legacy_namespace_deprecation"]
EXCLUDE = {".git","__pycache__","runtime_reports",".venv","venv"}

def _scan(root):
    base=Path(root); leg_hits=[]; can_hits=[]; leg_files=set(); can_files=set()
    for p in base.rglob("*.py"):
        rel=str(p)
        if any(x in rel for x in EXCLUDE): continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        for t in LEGACY:
            if t in text: leg_hits.append({"file":rel,"token":t,"lines":text.count(t)}); leg_files.add(rel)
        for t in CANONICAL:
            if t in text: can_hits.append({"file":rel,"token":t,"lines":text.count(t)}); can_files.add(rel)
    return {"legacy_hits":leg_hits,"canonical_hits":can_hits,"legacy_files":sorted(leg_files),"canonical_files":sorted(can_files)}

def _audit(leg_hits):
    violations=[]; allowed=[]
    for h in leg_hits:
        f=h["file"]; in_allow=any(k in f for k in ALLOW_KEYWORDS); in_block=any(k in f for k in BLOCK_KEYWORDS)
        if in_block and not in_allow and "legacy_namespace_deprecation" not in f: violations.append({**h,"reason":"LEGACY_IN_STRICTLY_BLOCKED"})
        elif not in_allow and not in_block: violations.append({**h,"reason":"LEGACY_OUTSIDE_ALLOWLIST"})
        else: allowed.append(h)
    return {"violations":violations,"allowed":allowed,"new_legacy_violation_count":len(violations)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="runtime_reports/v3519_legacy_namespace_deprecation_gate_report.json")
    args=ap.parse_args()
    
    print("Scanning namespace...",flush=True)
    scan=_scan(".")
    print(f"  Legacy: {len(scan['legacy_hits'])} hits in {len(scan['legacy_files'])} files",flush=True)
    print(f"  Canonical: {len(scan['canonical_hits'])} hits in {len(scan['canonical_files'])} files",flush=True)
    
    audit=_audit(scan["legacy_hits"])
    print(f"  New violations: {audit['new_legacy_violation_count']}",flush=True)
    if audit["violations"]:
        for v in audit["violations"][:5]:
            print(f"    {v['file']}: {v['token']} ({v['reason']})",flush=True)
    
    policies={"L0_DISPLAY_ONLY":{"new_legacy_allowed":False,"production_rewrite_allowed_now":False,"policy":"Rename after RC"},"L1_RESEARCH_ONLY":{"new_legacy_allowed":False,"production_rewrite_allowed_now":False,"policy":"Adapter-first canonical"},"L2_RISK_RELEVANT":{"new_legacy_allowed":False,"production_rewrite_allowed_now":False,"policy":"Safety passthrough only"},"L3_EXECUTION_CRITICAL":{"new_legacy_allowed":False,"production_rewrite_allowed_now":False,"policy":"Locked, no direct migration"},"UNKNOWN_RISK_TIER":{"new_legacy_allowed":False,"production_rewrite_allowed_now":False,"policy":"Manual review"}}

    can_adopt="PRESENT" if scan["canonical_hits"] else "MISSING"
    status="LEGACY_NAMESPACE_DEPRECATION_WARNING_LOCKED_LEGACY_REMAINS"
    if audit["new_legacy_violation_count"]>0: status="LEGACY_NAMESPACE_DEPRECATION_BLOCKED_NEW_LEGACY"

    report={"report_version":"V3519_LEGACY_NAMESPACE_DEPRECATION_GATE_REPORT_V10","mode":"PAPER_ONLY_DEPRECATION_GATE","namespace_scan":{"legacy_hit_count":len(scan["legacy_hits"]),"legacy_file_count":len(scan["legacy_files"]),"legacy_files":scan["legacy_files"][:50],"canonical_hit_count":len(scan["canonical_hits"]),"canonical_file_count":len(scan["canonical_files"]),"canonical_files":scan["canonical_files"][:30]},"legacy_namespace_diff_audit":{"new_legacy_violation_count":audit["new_legacy_violation_count"],"new_legacy_violations":audit["violations"][:50],"legacy_diff_status":"PASS" if not audit["violations"] else "NEW_LEGACY_DETECTED"},"canonical_namespace_audit":{"canonical_adoption_status":can_adopt,"canonical_hit_count":len(scan["canonical_hits"])},"deprecation_policy_matrix":{"policies":policies},"deprecation_gate_status":status,"recommended_next_step":"v3.5.20 Research OS RC","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"l2_l3_direct_migration_allowed":False,"legacy_namespace_expansion_allowed":False,"policy_violations":[]}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    
    print(f"\n  Legacy hits: {len(scan['legacy_hits'])} in {len(scan['legacy_files'])} files")
    print(f"  Canonical hits: {len(scan['canonical_hits'])} in {len(scan['canonical_files'])} files")
    print(f"  New violations: {audit['new_legacy_violation_count']}")
    print(f"  Canonical adoption: {can_adopt}")
    print(f"  Status: {status}")
    print(f"  Next: v3.5.20 Research OS RC")
    print("v3.5.19 done")

if __name__=="__main__": main()
