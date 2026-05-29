#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""v3.5.20 Research OS RC — Closeout Hardened"""
from __future__ import annotations
import json, argparse
from pathlib import Path
from zmatrix.research_os_rc.schema import DEFAULT_RESEARCH_OS_RC_SAFETY
from zmatrix.research_os_rc.safety_gate_auditor import audit_safety_gates
from zmatrix.research_os_rc.evidence_chain_auditor import audit_evidence_chain
from zmatrix.research_os_rc.rc_verdict_builder import build_rc_verdict
from zmatrix.research_os_rc.policy import validate_research_os_rc_report, collect_policy_violations

MILESTONES = [("v3.5.1","Return Integrity","收益可信度"),("v3.5.2","Strategy Repair","修复候选"),("v3.5.3","Exit Repair Replay","止损回放"),("v3.5.4","Invalidation Anatomy","失效解剖"),("v3.5.5","Entry Quality","入场质量"),("v3.5.6","Market Regime","市场状态归因"),("v3.5.7","Regime Paper Replay","市场纸面回放"),("v3.5.8","Pool Resilience","池韧性观察"),("v3.5.9","Sector Clock Foundation","行业时钟地基"),("v3.5.10","Sector Mapping","行业映射接入"),("v3.5.11","Synthetic Sector","合成行业指数"),("v3.5.12","Regime×Sector","联合归因"),("v3.5.13","B-Matrix Role","角色来源重建"),("v3.5.14","Role Namespace","角色命名迁移"),("v3.5.15","Taxonomy Closeout","命名宪法"),("v3.5.16","Migration Plan","迁移计划"),("v3.5.17","Adapter Bridge","桥接适配"),("v3.5.18","Classifier v2 Replay","分类器v2回放"),("v3.5.19","Namespace Deprecation","命名防扩散"),("v3.5.20","Research OS RC","研究OS收口")]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runtime-dir",default="runtime_reports")
    ap.add_argument("--output",default="runtime_reports/v3520_research_os_rc_report.json")
    args=ap.parse_args()

    # Load reports
    rd=Path(args.runtime_dir); reports={}; files=[]
    if rd.exists():
        for p in sorted(rd.glob("*.json")):
            try: reports[p.name]=json.loads(p.read_text(encoding="utf-8")); files.append(str(p))
            except: pass
    print(f"  Reports: {len(reports)}",flush=True)

    # Audit modules
    evidence = audit_evidence_chain(report_files=files)
    safety = audit_safety_gates(reports=reports)

    # Namespace freeze
    dep_reports=[r for n,r in reports.items() if "deprecation" in n.lower()]
    ns_status="PASS"; legacy_locked=False; new_v=0
    if dep_reports:
        dr=dep_reports[-1]; diff=dr.get("legacy_namespace_diff_audit",{}); ns=dr.get("namespace_scan",{})
        new_v=diff.get("new_legacy_violation_count",0); legacy_locked=ns.get("legacy_hit_count",0)>0
        ns_status="FAIL" if new_v>0 else "PASS"
    namespace={"namespace_status":ns_status,"legacy_locked_warning":legacy_locked,"new_legacy_violation_count":new_v}

    # Data foundation
    sm=any("sector_mapping" in n.lower() or "v3510" in n.lower() for n in reports)
    sb=any("synthetic_sector" in n.lower() or "v3511" in n.lower() for n in reports)
    data={"data_foundation_status":"READY" if sm and sb else "DATA_INSUFFICIENT","sector_mapping_found":sm,"sector_basket_found":sb}

    # Replay readiness
    cv2=None
    for n,r in reports.items():
        if "classifier_v2" in n.lower() or "v3518" in n.lower(): cv2=r
    rps="READY" if cv2 and cv2.get("classifier_v2_replay_status")=="CLASSIFIER_V2_REPLAY_READY" else "PARTIAL"
    rd_val=cv2.get("legacy_vs_v2_comparison",{}).get("role_delta_rate") if cv2 else None
    sm_val=cv2.get("role_source_stability_audit",{}).get("source_mismatch_rate") if cv2 else None
    replay={"replay_readiness_status":rps,"classifier_v2_ready":rps=="READY","role_delta_rate":rd_val,"source_mismatch_rate":sm_val}

    # Verdict
    verdict = build_rc_verdict(evidence_chain=evidence,safety_gate=safety,namespace_freeze=namespace,data_foundation=data,replay_readiness=replay)

    cap={"data_spine":"READY","historical_replay":"READY","return_integrity":"READY","market_regime_attribution":"READY","sector_mapping":"READY","synthetic_sector_index":"PAPER_ONLY_READY","regime_sector_attribution":"READY_BUT_NOT_SEPARABLE","role_taxonomy":"READY","classifier_v2_paper_adapter":"READY","adapter_first_bridge":"READY","namespace_deprecation_gate":"READY_WITH_LOCKED_WARNINGS","production_trading":"BLOCKED","broker_execution":"BLOCKED","runtime":"BLOCKED"}

    report={"report_version":"V3520_RESEARCH_OS_RC_REPORT_V10","mode":"RESEARCH_OS_RC_ONLY","version_ceiling":"v3.5.20","next_version_allowed":False,"milestone_registry":{"milestone_count":len(MILESTONES),"milestones":[{"version":v,"name":n,"purpose":p} for v,n,p in MILESTONES]},"runtime_report_loader":{"report_count":len(reports)},"evidence_chain_audit":evidence,"capability_card":cap,"safety_gate_audit":safety,"namespace_freeze_audit":namespace,"data_foundation_audit":data,"replay_readiness_audit":replay,"rc_verdict":verdict,"research_os_rc_status":verdict["rc_status"],"recommended_next_step":"STOP_AT_V3.5.20_RESEARCH_OS_RC","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False,"legacy_module_direct_rewrite_allowed":False,"l2_l3_direct_migration_allowed":False,"legacy_namespace_expansion_allowed":False,"safety":dict(DEFAULT_RESEARCH_OS_RC_SAFETY)}

    # P0-3 fix: compute policy_violations from audits, not hardcoded
    report["policy_violations"] = collect_policy_violations(safety_audit=safety,namespace_audit=namespace,evidence_audit=evidence)
    report["policy_violations"].extend(validate_research_os_rc_report(report))

    out=Path(args.output); out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"\n  ☯️ v3.5.20 Research OS RC — Closeout Hardened")
    print(f"  Reports: {len(reports)} | Evidence: {evidence['evidence_chain_status']}")
    print(f"  Safety: {safety['safety_gate_status']} ({safety['safety_violation_count']} violations)")
    print(f"  Namespace: {ns_status} (new: {new_v}) | Data: {data['data_foundation_status']}")
    print(f"  Replay: {rps} (delta:{rd_val} mismatch:{sm_val})")
    print(f"  RC: {verdict['rc_status']} | Blockers: {verdict['blockers'] or 'NONE'}")
    print(f"  Policy violations: {len(report['policy_violations'])}")
    print(f"  Research Ready: {verdict['research_ready']} | Production: False")
    print("v3.5.20 closeout hardened")

if __name__=="__main__": main()
