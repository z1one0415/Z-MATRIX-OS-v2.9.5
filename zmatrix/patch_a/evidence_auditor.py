"""PATCH-A-7: Evidence Chain Status Auditor — 从文件名验证升级为状态字段验证"""
from __future__ import annotations

REQUIRED_EVIDENCE_STATUS = {"v3518_classifier_v2_replay": {"field":"classifier_v2_replay_status","valid":["CLASSIFIER_V2_REPLAY_READY"]},"v3519_namespace_deprecation": {"field":"deprecation_gate_status","valid":["LEGACY_NAMESPACE_DEPRECATION_GATE_READY","LEGACY_NAMESPACE_DEPRECATION_WARNING_LOCKED_LEGACY_REMAINS"]},"v3510_sector_mapping": {"field":"ingestion_status","valid":["SECTOR_MAPPING_READY"]},"v3511_sector_basket": {"field":"basket_status","valid":["SYNTHETIC_SECTOR_BASKET_READY"]},"v3520_rc": {"field":"research_os_rc_status","valid":["RESEARCH_OS_RC_READY_WITH_LOCKED_WARNINGS","RESEARCH_OS_RC_READY"]}}

def audit_evidence_status(*, reports: dict) -> dict:
    results = {}
    for report_key, cfg in REQUIRED_EVIDENCE_STATUS.items():
        found = False; status = None
        for name, r in (reports or {}).items():
            if not isinstance(r, dict): continue
            if report_key.split("_")[0][1:] in name.lower() or any(k in name.lower() for k in report_key.split("_")[:3]):
                actual = r.get(cfg["field"])
                if actual in cfg["valid"]: found = True; status = actual
                break
        results[report_key] = {"passed": found, "actual_status": status, "required_field": cfg["field"], "accepted_values": cfg["valid"]}
    passed = sum(1 for r in results.values() if r["passed"])
    return {"auditor_version":"PATCH_A_EVIDENCE_STATUS_AUDITOR_V10","results":results,"passed_count":passed,"total_count":len(results),"evidence_chain_status":"READY" if passed == len(results) else "MISSING_EVIDENCE","method":"STATUS_FIELD_VALIDATION","previous_method":"FILENAME_ONLY","upgrade_note":"Evidence chain now validates internal report status fields, not just file existence"}

LEGACY_REPORT_RECLASSIFICATION = {"v357_regime_replay_bull_only":"HISTORICAL_READY_PENDING_OUTCOME_HORIZON_RECHECK","v357_regime_replay_range_obs":"HISTORICAL_READY_PENDING_OUTCOME_HORIZON_RECHECK","v355_entry_quality":"QUARANTINED_BY_OUTCOME_HORIZON","v353_exit_repair":"DEPRECATED_METRICS","v354_invalidation_anatomy":"DEPRECATED_METRICS","v356_regime_attribution":"READY_PENDING_HORIZON_RECHECK","v3512_regime_sector":"READY_PENDING_HORIZON_RECHECK"}
