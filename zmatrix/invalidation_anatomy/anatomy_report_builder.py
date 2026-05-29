# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.invalidation_anatomy.invalidation_event_builder import build_invalidation_event, _load_price_bars
from zmatrix.invalidation_anatomy.post_invalidation_path_labeler import label_post_invalidation_path
from zmatrix.invalidation_anatomy.pre_trigger_feature_builder import build_pre_trigger_features
from zmatrix.invalidation_anatomy.trigger_day_feature_builder import build_trigger_day_features
from zmatrix.invalidation_anatomy.recovery_profile_classifier import build_recovery_profile
from zmatrix.invalidation_anatomy.beta_shakeout_detector import detect_beta_shakeout
from zmatrix.invalidation_anatomy.separability_tester import test_path_separability
from zmatrix.invalidation_anatomy.rule_candidate_miner import mine_conditional_invalidation_candidates
from zmatrix.invalidation_anatomy.policy import validate_invalidation_anatomy_report
from zmatrix.invalidation_anatomy.schema import DEFAULT_INVALIDATION_ANATOMY_SAFETY

def build_invalidation_anatomy_report(*, joined: list[dict], data_root: str = ".", max_items: int | None = None) -> dict:
    items = joined[:max_items] if max_items else joined; rows = []
    for sample in items:
        bars = _load_price_bars(sample.get("ticker") or "", sample.get("entry_date", ""), data_root, 80)
        event = build_invalidation_event(sample=sample, price_bars=bars)
        if event.get("event_status") != "READY": continue
        label = label_post_invalidation_path(event=event, price_bars=bars)
        pre = build_pre_trigger_features(event=event, price_bars=bars)
        trigger = build_trigger_day_features(event=event, price_bars=bars)
        recovery = build_recovery_profile(event=event, price_bars=bars)
        beta = detect_beta_shakeout(event=event)
        features = {}; features.update(pre.get("features", {})); features.update(trigger.get("features", {}))
        features.update({k: v for k, v in recovery.items() if k.startswith("rebound_after_trigger")}); features.update({"is_beta_shakeout_candidate": beta.get("is_beta_shakeout_candidate")})
        rows.append({"paper_id": sample.get("paper_id"), "ticker": sample.get("ticker"), "event": event, "path_label": label, "path_type": label.get("path_type"), "pre_trigger_features": pre, "trigger_day_features": trigger, "recovery_profile": recovery, "beta_shakeout": beta, "features": features})
    path_counts = {}
    for r in rows:
        pt = r.get("path_type") or "UNKNOWN_PATH"
        path_counts[pt] = path_counts.get(pt, 0) + 1
    separability = test_path_separability(anatomy_rows=rows)
    candidates = mine_conditional_invalidation_candidates(separability_report=separability)
    report = {"report_version": "V354_INVALIDATION_ANATOMY_REPORT_V10", "mode": "ANATOMY_ONLY", "input_count": len(items), "invalidation_event_count": len(rows), "invalidation_event_rate": len(rows) / len(items) if items else None, "path_type_counts": path_counts, "separability": separability, "conditional_invalidation_candidates": candidates, "sample_rows": rows[:100], "production_strategy_modified": False, "real_trade_allowed": False, "broker_order_allowed": False, "auto_buy_allowed": False, "auto_sell_allowed": False, "auto_position_close_allowed": False, "runtime_enabled": False, "safety": dict(DEFAULT_INVALIDATION_ANATOMY_SAFETY)}
    report["policy_violations"] = validate_invalidation_anatomy_report(report)
    return report
