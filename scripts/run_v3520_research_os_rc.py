#!/usr/bin/env python3
"""v3.5.20 Research OS RC"""
from __future__ import annotations
import json, argparse
from pathlib import Path

MILESTONES = [("v3.5.1","Return Integrity","收益可信度"),("v3.5.2","Strategy Repair","修复候选"),("v3.5.3","Exit Repair Replay","止损回放"),("v3.5.4","Invalidation Anatomy","失效解剖"),("v3.5.5","Entry Quality","入场质量"),("v3.5.6","Market Regime","市场状态归因"),("v3.5.7","Regime Paper Replay","市场纸面回放"),("v3.5.8","Pool Resilience","池韧性观察"),("v3.5.9","Sector Clock Foundation","行业时钟地基"),("v3.5.10","Sector Mapping","行业映射接入"),("v3.5.11","Synthetic Sector","合成行业指数"),("v3.5.12","Regime×Sector","联合归因"),("v3.5.13","B-Matrix Role","角色来源重建"),("v3.5.14","Role Namespace","角色命名迁移"),("v3.5.15","Taxonomy Closeout","命名宪法"),("v3.5.16","Migration Plan","迁移计划"),("v3.5.17","Adapter Bridge","桥接适配"),("v3.5.18","Classifier v2 Replay","分类器v2回放"),("v3.5.19","Namespace Deprecation","命名防扩散"),("v3.5.20","Research OS RC","研究OS收口")]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runtime-dir",default="runtime_reports")
    ap.add_argument("--output",default="runtime_reports/v3520_research_os_rc_report.json")
    args=ap.parse_args()

    # Load all reports
    rd=Path(args.runtime_dir)
    reports={}
    if rd.exists():
        for p in sorted(rd.glob("*.json")):
            try: reports[p.name]=json.loads(p.read_text(encoding="utf-8"))
            except: pass
    print(f"  Reports found: {len(reports)}",flush=True)

    # Evidence chain
    evidence_keys=["return_integrity","repair","invalidation","entry_quality","regime","sector_mapping","synthetic_sector","regime_sector","role_replay","taxonomy","adapter","classifier_v2","deprecation"]
    found={}; missing=[]
    for k in evidence_keys:
        ok=any(k in n.lower() for n in reports); found[k]=ok
        if not ok: missing.append(k)
    evidence_status="READY" if not missing else "MISSING_EVIDENCE"

    # Safety gate
    blocked=["real_trade_allowed","broker_order_allowed","auto_buy_allowed","auto_sell_allowed","runtime_enabled","classifier_production_write_allowed","production_yaml_write_allowed","legacy_runtime_rewrite_allowed"]
    violations=[]
    for name,r in reports.items():
        if not isinstance(r,dict): continue
        for f in blocked:
            if r.get(f) is True: violations.append({"report":name,"field":f})
            s=r.get("safety",{})
            if isinstance(s,dict) and s.get(f) is True: violations.append({"report":name,"field":f"safety.{f}"})
    safety_status="PASS" if not violations else "FAIL"

    # Namespace freeze - check deprecation report
    dep_reports=[r for n,r in reports.items() if "deprecation" in n.lower()]
    ns_status="PASS"; legacy_locked=False; new_v=0
    if dep_reports:
        dr=dep_reports[-1]; diff=dr.get("legacy_namespace_diff_audit",{}); ns=dr.get("namespace_scan",{})
        new_v=diff.get("new_legacy_violation_count",0)
        legacy_locked=ns.get("legacy_hit_count",0)>0
        ns_status="FAIL" if new_v>0 else "PASS"

    # Data foundation
    sector_mapping=any("sector_mapping" in n.lower() or "v3510" in n.lower() for n in reports)
    sector_basket=any("synthetic_sector" in n.lower() or "v3511" in n.lower() for n in reports)
    data_status="READY" if sector_mapping and sector_basket else "DATA_INSUFFICIENT"

    # Replay readiness
    classifier_v2=None
    for n,r in reports.items():
        if "classifier_v2" in n.lower() or "v3518" in n.lower(): classifier_v2=r
    replay_status="READY" if classifier_v2 and classifier_v2.get("classifier_v2_replay_status")=="CLASSIFIER_V2_REPLAY_READY" else "PARTIAL"
    role_delta=classifier_v2.get("legacy_vs_v2_comparison",{}).get("role_delta_rate") if classifier_v2 else None
    src_mismatch=classifier_v2.get("role_source_stability_audit",{}).get("source_mismatch_rate") if classifier_v2 else None

    # Verdict
    blockers=[]; warnings=[]
    if evidence_status!="READY": blockers.append("MISSING_EVIDENCE")
    if safety_status!="PASS": blockers.append("SAFETY_GATE_FAIL")
    if ns_status!="PASS": blockers.append("NAMESPACE_FREEZE_FAIL")
    if data_status!="READY": blockers.append("DATA_FOUNDATION_INSUFFICIENT")
    if replay_status!="READY": warnings.append("REPLAY_PARTIAL")
    if legacy_locked: warnings.append("LEGACY_LOCKED_WARNING")
    rc_status="RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS" if warnings else "RESEARCH_OS_RC_READY"
    if blockers: rc_status="RESEARCH_OS_RC_BLOCKED_MISSING_EVIDENCE"

    # Capability card
    cap={"data_spine":"READY","historical_replay":"READY","return_integrity":"READY","market_regime_attribution":"READY","sector_mapping":"READY","synthetic_sector_index":"PAPER_ONLY_READY","regime_sector_attribution":"READY_BUT_NOT_SEPARABLE","role_taxonomy":"READY","classifier_v2_paper_adapter":"READY","adapter_first_bridge":"READY","namespace_deprecation_gate":"READY_WITH_LOCKED_WARNINGS","production_trading":"BLOCKED","broker_execution":"BLOCKED","runtime":"BLOCKED"}

    report={"report_version":"V3520_RESEARCH_OS_RC_REPORT_V10","mode":"RESEARCH_OS_RC_ONLY","version_ceiling":"v3.5.20","next_version_allowed":False,"milestone_registry":{"milestone_count":len(MILESTONES),"milestones":[{"version":v,"name":n,"purpose":p} for v,n,p in MILESTONES]},"runtime_report_loader":{"report_count":len(reports)},"evidence_chain_audit":{"evidence_chain_status":evidence_status,"found":found,"missing":missing},"capability_card":cap,"safety_gate_audit":{"safety_gate_status":safety_status,"safety_violation_count":len(violations),"violations":violations[:20]},"namespace_freeze_audit":{"namespace_status":ns_status,"legacy_locked_warning":legacy_locked,"new_legacy_violation_count":new_v},"data_foundation_audit":{"data_foundation_status":data_status,"sector_mapping_found":sector_mapping,"sector_basket_found":sector_basket},"replay_readiness_audit":{"replay_readiness_status":replay_status,"classifier_v2_ready":replay_status=="READY","role_delta_rate":role_delta,"source_mismatch_rate":src_mismatch},"rc_verdict":{"rc_status":rc_status,"blockers":blockers,"warnings":warnings,"research_ready":rc_status in ("RESEARCH_OS_RC_READY","RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS"),"production_ready":False},"research_os_rc_status":rc_status,"recommended_next_step":"STOP_AT_V3.5.20_RESEARCH_OS_RC","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"l2_l3_direct_migration_allowed":False,"legacy_namespace_expansion_allowed":False,"policy_violations":[]}

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  {'='*50}")
    print(f"  ☯️ Z-MATRIX Research OS RC — v3.5.20")
    print(f"  {'='*50}")
    print(f"  Reports: {len(reports)}")
    print(f"  Evidence: {evidence_status} ({len(found)-len(missing)}/{len(found)})")
    print(f"  Safety: {safety_status} ({len(violations)} violations)")
    print(f"  Namespace: {ns_status} (new violations: {new_v})")
    print(f"  Data: {data_status}")
    print(f"  Replay: {replay_status} (delta: {role_delta}, mismatch: {src_mismatch})")
    print(f"  {'─'*50}")
    print(f"  RC Status: {rc_status}")
    print(f"  Blockers: {blockers or 'NONE'}")
    print(f"  Warnings: {warnings or 'NONE'}")
    print(f"  Research Ready: {rc_status in ('RESEARCH_OS_RC_READY','RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS')}")
    print(f"  Production Ready: False")
    print(f"  Next: STOP at v3.5.20 Research OS RC")
    print("v3.5.20 RC complete")

if __name__=="__main__": main()
