#!/usr/bin/env python3
"""v3.5.16 Legacy Locked Module Migration Plan"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from collections import Counter

LEGACY_TOKENS = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","WATCH_ONLY"]
WRITE_PATTERNS = ["=",".update(","write","save","persist","commit","apply","modify"]
EXCLUDE = {".git","__pycache__","runtime_reports",".venv","venv","tests","data","node_modules"}

def _scan(root):
    base=Path(root); files=[]
    for p in base.rglob("*.py"):
        rel=str(p)
        if any(x in rel for x in EXCLUDE): continue
        text=p.read_text(encoding="utf-8",errors="ignore")
        tokens=[t for t in LEGACY_TOKENS if t in text]
        if tokens: files.append({"file":rel,"tokens":tokens,"line_count":len(text.splitlines())})
    return sorted(files,key=lambda x:x["file"])

def _classify_usage(f):
    low=f["file"].lower()
    if "test" in low: return "TEST_OR_FIXTURE"
    if "report" in low or "audit" in low or "dashboard" in low or "monthly_review" in low: return "REPORT_OR_AUDIT"
    if "pre_trade" in low or "position" in low or "z8" in low: return "EXECUTION_OR_POSITION_CONTROL"
    if "risk" in low or "constitution" in low or "policy" in low: return "RISK_OR_ACCOUNT_POLICY"
    if "replay" in low or "research" in low or "strategy_validation" in low or "attribution" in low or "repair" in low or "observation" in low or "ingestion" in low or "dry_run" in low or "rehearsal" in low: return "RESEARCH_OR_REPLAY"
    if "gate" in low or "registry" in low or "pipeline" in low or "workflow" in low: return "ARCHITECTURE_OR_GATE"
    if "scoring" in low or "band" in low or "matrix" in low or "classifier" in low: return "MATRIX_OR_CLASSIFIER"
    return "UNKNOWN_USAGE"

def _usage_to_tier(usage):
    return {"REPORT_OR_AUDIT":"L0_DISPLAY_ONLY","TEST_OR_FIXTURE":"L1_RESEARCH_ONLY","RESEARCH_OR_REPLAY":"L1_RESEARCH_ONLY","ARCHITECTURE_OR_GATE":"L1_RESEARCH_ONLY","MATRIX_OR_CLASSIFIER":"L1_RESEARCH_ONLY","RISK_OR_ACCOUNT_POLICY":"L2_RISK_RELEVANT","EXECUTION_OR_POSITION_CONTROL":"L3_EXECUTION_CRITICAL"}.get(usage,"UNKNOWN_RISK_TIER")

def _adapter(tier):
    return {"L0_DISPLAY_ONLY":"OPTIONAL_DISPLAY_ADAPTER","L1_RESEARCH_ONLY":"RESEARCH_ROLE_ADAPTER","L2_RISK_RELEVANT":"RISK_SAFE_ROLE_BRIDGE","L3_EXECUTION_CRITICAL":"EXECUTION_COMPATIBILITY_BRIDGE"}.get(tier,"MANUAL_REVIEW_REQUIRED")

def _migration_mode(tier):
    return {"L0_DISPLAY_ONLY":"DIRECT_RENAME_ALLOWED_LATER","L1_RESEARCH_ONLY":"ADAPTER_FIRST","L2_RISK_RELEVANT":"ADAPTER_FIRST_WITH_REGRESSION","L3_EXECUTION_CRITICAL":"NO_DIRECT_REWRITE"}.get(tier,"BLOCK_UNTIL_REVIEW")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="runtime_reports/v3516_legacy_locked_module_migration_plan.json")
    args=ap.parse_args()
    print("Scanning legacy modules...",flush=True)
    files=_scan(".")
    print(f"  {len(files)} legacy files found",flush=True)
    
    # Classify
    classified=[]; tier_counts=Counter(); write_risks=[]; adapter_plans=[]; phases={"L0":[],"L1":[],"L2":[],"L3":[],"UNKNOWN":[]}
    for f in files:
        u=_classify_usage(f); tier=_usage_to_tier(u); tier_counts[tier]+=1
        # Write risk
        try:
            text=Path(f["file"]).read_text(encoding="utf-8",errors="ignore"); has_write=any(p in text for p in WRITE_PATTERNS)
        except: has_write=False
        wr="HIGH_WRITE_RISK" if tier in ("L2_RISK_RELEVANT","L3_EXECUTION_CRITICAL") and has_write else "LOW_OR_UNKNOWN"
        if wr=="HIGH_WRITE_RISK": write_risks.append({"file":f["file"],"tier":tier,"has_write":has_write})
        # Adapter
        ap=_adapter(tier); mm=_migration_mode(tier)
        plan={"file":f["file"],"tokens":f["tokens"],"usage_type":u,"risk_tier":tier,"adapter_required":ap,"migration_mode":mm,"production_rewrite_allowed":False}
        adapter_plans.append(plan); phases[tier.split("_")[0]].append(plan)
        classified.append(plan)
    
    report={"report_version":"V3516_LEGACY_LOCKED_MODULE_MIGRATION_PLAN_REPORT_V10","mode":"PLANNING_ONLY","legacy_inventory":{"legacy_file_count":len(files),"legacy_files_sample":files[:50]},"risk_tier_classification":{"risk_tier_counts":dict(tier_counts),"classified":classified[:30]},"write_risk_audit":{"high_write_risk_count":len(write_risks),"high_write_risk_files":write_risks[:20],"legacy_module_direct_rewrite_allowed":False},"migration_sequence":{"phases":{"phase_1_display":phases["L0"],"phase_2_research":phases["L1"],"phase_3_risk_bridges":phases["L2"],"phase_4_execution_locked":phases["L3"],"manual_review":phases["UNKNOWN"]},"direct_rewrite_allowed":False},"recommended_next_step":"v3.5.17 Adapter-First Paper Integration" if not write_risks else "v3.5.17 Execution/Risk Bridge Design","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"policy_violations":[],"migration_status":"LEGACY_MIGRATION_PLAN_READY" if not write_risks else "LEGACY_MIGRATION_BLOCKED"}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    
    print(f"\n  Legacy files: {len(files)}")
    print(f"  Risk tiers: {dict(tier_counts)}")
    print(f"  High write risk: {len(write_risks)}")
    print(f"  Phases: L0={len(phases['L0'])} L1={len(phases['L1'])} L2={len(phases['L2'])} L3={len(phases['L3'])}")
    print(f"  Status: {report['migration_status']}")
    print(f"  Next: {report['recommended_next_step']}")
    print("v3.5.16 done")

if __name__=="__main__": main()
