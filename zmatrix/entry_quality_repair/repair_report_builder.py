# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.entry_quality_repair.entry_feature_builder import build_entry_features
from zmatrix.entry_quality_repair.entry_quality_scorer import score_entry_quality
from zmatrix.entry_quality_repair.b_rotation_archetype_classifier import classify_b_rotation_archetype
from zmatrix.entry_quality_repair.entry_rule_replay import run_entry_rule_replay
from zmatrix.entry_quality_repair.candidate_verdict import judge_all_entry_candidates
from zmatrix.entry_quality_repair.policy import validate_entry_quality_repair_report
from zmatrix.entry_quality_repair.schema import DEFAULT_ENTRY_REPAIR_SAFETY

def build_entry_quality_repair_report(*, joined: list[dict], data_root: str = ".", horizon: str = "t20", max_items: int | None = None) -> dict:
    items = joined[:max_items] if max_items else joined; enriched = []
    for sample in items:
        feat = build_entry_features(sample=sample, data_root=data_root)
        if feat.get("feature_status") != "READY": continue
        features = feat.get("features",{})
        score = score_entry_quality(features=features)
        arch = classify_b_rotation_archetype(features=features, entry_quality_score=score.get("entry_quality_score"))
        enriched.append({**sample,"entry_features":features,"entry_quality_score":score.get("entry_quality_score"),"entry_quality_bucket":score.get("entry_quality_bucket"),"entry_quality_reasons":score.get("reason_codes"),"entry_archetype":arch.get("archetype")})
    ac={}; qc={}
    for row in enriched:
        a=row.get("entry_archetype"); b=row.get("entry_quality_bucket")
        ac[a]=ac.get(a,0)+1; qc[b]=qc.get(b,0)+1
    replay = run_entry_rule_replay(enriched_rows=enriched, horizon=horizon)
    verdict = judge_all_entry_candidates(replay=replay)
    report = {"report_version":"V355_ENTRY_QUALITY_REPAIR_REPORT_V10","mode":"PAPER_ONLY_ENTRY_REPAIR","input_count":len(items),"feature_ready_count":len(enriched),"feature_ready_rate":len(enriched)/len(items) if items else None,"archetype_counts":ac,"entry_quality_bucket_counts":qc,"entry_rule_replay":replay,"candidate_verdict":verdict,"ready_candidates":verdict.get("ready_candidates",[]),"sample_enriched_rows":enriched[:100],"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_ENTRY_REPAIR_SAFETY)}
    report["policy_violations"] = validate_entry_quality_repair_report(report)
    return report
