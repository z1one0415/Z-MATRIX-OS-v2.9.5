#!/usr/bin/env python3
"""v3.5.15 Role Taxonomy Closeout + Classifier v2 Paper Adapter"""
from __future__ import annotations
import json, argparse
from pathlib import Path

LEGACY_LOCKED = ["account_constitution.py","pre_trade_checklist.py","z8_position_control.py","brd_result_audit","brd_strategy_validation","b_matrix_pit_builder.py","gate_registry.py","skill_registry.py","classifier_interface.py","paper_action_builder.py","brd_replay","lightweight_backtest.py","ledger.py","investment_role_workflow.py","b_matrix.py","real_brd_connector.py","hibernate_mode.py","d_matrix_freeze.py","limit_down_blackhole.py","wakeup_probation.py","domestic_liquidity_crash.py","monthly_review.py","rehearsal_runner.py","replay_engine.py","dataset_loader.py","o3_conditional_fallback_planner.py","regime_candidate_miner.py","discover_brd_classifier_candidates","entry_quality_repair","regime_attribution","return_integrity","regime_conditioned_replay","strategy_repair","regime_observation","scoring","run_v351","run_v352","run_v353","run_v354","run_v355","run_v356","run_v357","run_v3510","run_v3511","run_v3512","run_v3513","stock_role_classifier.py","schema.py"]
LEGACY_TOKENS = ["A_LONG_CORE","B_MID_ROTATION","C_SHORT_EVENT","D_REJECT","WATCH_ONLY"]
CANONICAL_TOKENS = ["ROLE_CORE","ROLE_ROT","ROLE_HUNT","ROLE_WATCH","ROLE_BLOCK"]
BLOCKED_FIELDS = ["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed","auto_position_close_allowed","real_z9_write_allowed","hermes_memory_write_allowed","auto_calibration_allowed","prompt_auto_injection_allowed","system_prompt_write_allowed","runtime_injection_allowed","runtime_enabled","external_api_default_on","production_yaml_write_allowed","production_parameter_write_allowed","classifier_production_write_allowed","role_definition_production_write_allowed","legacy_runtime_rewrite_allowed"]

def _scan(root="."):
    base = Path(root); legacy_hits=[]; canonical_hits=[]
    exclude = {".git","__pycache__","runtime_reports",".venv","venv","tests"}
    for p in base.rglob("*.py"):
        rel = str(p)
        if any(x in rel for x in exclude): continue
        text = p.read_text(encoding="utf-8",errors="ignore")
        for t in LEGACY_TOKENS:
            if t in text: legacy_hits.append({"file":rel,"token":t,"locked":any(x in rel for x in LEGACY_LOCKED)})
        for t in CANONICAL_TOKENS:
            if t in text: canonical_hits.append({"file":rel,"token":t})
    violations = [h for h in legacy_hits if not h["locked"] and "role_taxonomy_closeout" not in h["file"] and "role_replay" not in h["file"]]
    return {"legacy_hit_count":len(legacy_hits),"canonical_hit_count":len(canonical_hits),"legacy_hits_sample":legacy_hits[:50],"canonical_hits_sample":canonical_hits[:30],"legacy_namespace_violations":violations[:50],"legacy_namespace_violation_count":len(violations),"scan_status":"PASS" if not violations else "LEGACY_NAMESPACE_VIOLATION"}

def _run_smoke():
    results=[]
    tests=[{"name":"b_pass_core","args":{"ticker":"000001","b_matrix":{"status":"PASS"},"r_matrix":{"status":"PASS"},"d_matrix":{"status":"FAIL"}},"expected":"ROLE_CORE"},{"name":"r_pass_rot","args":{"ticker":"000002","b_matrix":{"status":"FAIL"},"r_matrix":{"status":"PASS"},"d_matrix":{"status":"FAIL"}},"expected":"ROLE_ROT"},{"name":"d_pass_hunt","args":{"ticker":"000003","b_matrix":{"status":"FAIL"},"r_matrix":{"status":"FAIL"},"d_matrix":{"status":"PASS"}},"expected":"ROLE_HUNT"},{"name":"all_fail_block","args":{"ticker":"000004","b_matrix":{"status":"FAIL"},"r_matrix":{"status":"FAIL"},"d_matrix":{"status":"FAIL"}},"expected":"ROLE_BLOCK"}]
    for s in tests:
        out = _classify(**s["args"])
        results.append({"name":s["name"],"expected_role":s["expected"],"actual_role":out.get("canonical_role"),"pass":out["canonical_role"]==s["expected"],"source_matrix":out.get("source_matrix"),"production_ready":out.get("production_ready")})
    ok = all(x["pass"] for x in results)
    return {"adapter_status":"PASS" if ok else "FAIL","results":results,"production_ready":False}

def _pass(m): return m.get("status")=="PASS" or m.get("matrix_status")=="PASS"

def _classify(*,ticker,b_matrix=None,r_matrix=None,d_matrix=None):
    b=b_matrix or {}; r=r_matrix or {}; d=d_matrix or {}
    bp=_pass(b); rp=_pass(r); dp=_pass(d)
    if bp and rp: role="ROLE_CORE"; src="MATRIX_B_BASE"
    elif bp: role="ROLE_CORE"; src="MATRIX_B_BASE"
    elif rp and not bp: role="ROLE_ROT"; src="MATRIX_R_ROTATION"
    elif dp: role="ROLE_HUNT"; src="MATRIX_D_DARK_HORSE"
    else: role="ROLE_BLOCK"; src="NONE"
    return {"canonical_role":role,"source_matrix":src,"production_ready":False,"classifier_production_write_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--output", default="runtime_reports/v3515_role_taxonomy_closeout_report.json")
    args = ap.parse_args()
    scan = _scan(".")
    smoke = _run_smoke()
    manifest = {"locked_modules":[{"module":m,"legacy_allowed":True,"production_rewrite_allowed":False,"migration_required":True} for m in LEGACY_LOCKED],"locked_count":len(LEGACY_LOCKED)}

    blockers=[]; warnings=[]
    if scan["legacy_namespace_violation_count"]>0: blockers.append("UNLOCKED_LEGACY_NAMESPACE_VIOLATION")
    if smoke["adapter_status"]!="PASS": blockers.append("CLASSIFIER_V2_ADAPTER_SMOKE_FAILED")
    if manifest["locked_count"]>0: warnings.append("LEGACY_MODULES_LOCKED")
    readiness = "MIGRATION_BLOCKED" if blockers else "MIGRATION_READY_WITH_LEGACY_LOCKS" if warnings else "MIGRATION_READY"
    status = "ROLE_TAXONOMY_WARNING_LEGACY_LOCKED" if warnings else "ROLE_TAXONOMY_CLOSEOUT_READY"
    if blockers: status = "ROLE_TAXONOMY_BLOCKED_POLICY_VIOLATION"

    report = {"report_version":"V3515_ROLE_TAXONOMY_CLOSEOUT_REPORT_V10","mode":"PAPER_ONLY_ROLE_TAXONOMY_CLOSEOUT","classifier_v2_paper_adapter_smoke":smoke,"namespace_scan":scan,"legacy_lock_manifest":manifest,"migration_readiness":{"readiness_status":readiness,"blockers":blockers,"warnings":warnings},"taxonomy_closeout_status":status,"recommended_next_step":"v3.5.16 Classifier v2 Paper Replay" if status=="ROLE_TAXONOMY_CLOSEOUT_READY" else "v3.5.16 Legacy Locked Module Migration Plan" if status=="ROLE_TAXONOMY_WARNING_LEGACY_LOCKED" else "Fix violations","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"policy_violations":[],"taxonomy":{"matrices":["MATRIX_B_BASE","MATRIX_R_ROTATION","MATRIX_D_DARK_HORSE"],"roles":["ROLE_CORE","ROLE_ROT","ROLE_HUNT","ROLE_WATCH","ROLE_BLOCK"],"actions":["ACTION_HOLD_CORE","ACTION_PAPER_ROT","ACTION_PAPER_HUNT","ACTION_WATCH_ONLY","ACTION_BLOCK"],"principle":"Matrix=B/R/D evidence; Role=CORE/ROT/HUNT/WATCH/BLOCK account; Action=execution"}}

    if scan["legacy_namespace_violation_count"]>0 and status!="MIGRATION_BLOCKED":
        report["policy_violations"].extend([f"{v['file']}:{v['token']}" for v in scan["legacy_namespace_violations"][:10]])

    out = Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  v3.5.15 Role Taxonomy Closeout")
    print(f"  Smoke: {smoke['adapter_status']}")
    print(f"  Scan: {scan['legacy_hit_count']} legacy hits, {scan['canonical_hit_count']} canonical hits")
    print(f"  Violations: {scan['legacy_namespace_violation_count']} (unlocked non-migration)")
    print(f"  Locked modules: {manifest['locked_count']}")
    print(f"  Readiness: {readiness}")
    print(f"  Status: {status}")
    print(f"  Next: {report['recommended_next_step']}")
    print("v3.5.15 done")

if __name__ == "__main__": main()
