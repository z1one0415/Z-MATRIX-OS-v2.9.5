# allowlist: forbidden-token-definition
from __future__ import annotations

REPAIR_CANDIDATE_RULES = {
    "exclude_invalidated": {"description": "Remove samples that triggered invalidation.", "lookahead_risk": False},
    "exclude_high_mae": {"description": "Remove samples with max adverse excursion below -10%.", "lookahead_risk": True, "note": "MAE is known after entry; use only for diagnosis unless converted into stop rule."},
    "exclude_extreme_right_tail_for_metric_only": {"description": "Exclude extreme winners to test tail dependency.", "lookahead_risk": True, "metric_only": True},
    "keep_only_non_invalidated_b_rotation": {"description": "Keep B_MID_ROTATION samples that did not trigger invalidation.", "lookahead_risk": True},
    "require_positive_t5_confirmation": {"description": "Require T5 return > 0 before continuing to T20.", "lookahead_risk": True, "note": "Can only be modeled as staged confirmation, not original entry filter."},
}

def apply_candidate_rule(*, joined: list[dict], rule_name: str) -> dict:
    rule = REPAIR_CANDIDATE_RULES[rule_name]
    kept = []
    for x in joined or []:
        if x.get("outcome_status") != "READY": continue
        if x.get("paper_action") in ("NO_ACTION", "DATA_GAP", None): continue
        if rule_name == "exclude_invalidated":
            if x.get("invalidation_triggered") is True: continue
        elif rule_name == "exclude_high_mae":
            mae = x.get("max_adverse_excursion_pct")
            if mae is not None and float(mae) < -10: continue
        elif rule_name == "exclude_extreme_right_tail_for_metric_only":
            r = x.get("actual_return_t20")
            if r is not None and float(r) > 120: continue
        elif rule_name == "keep_only_non_invalidated_b_rotation":
            if x.get("role") != "B_MID_ROTATION": continue
            if x.get("invalidation_triggered") is True: continue
        elif rule_name == "require_positive_t5_confirmation":
            r5 = x.get("actual_return_t5")
            if r5 is None or float(r5) <= 0: continue
        kept.append(x)
    return {"rule_name": rule_name, "rule": rule, "original_count": len(joined or []), "kept_count": len(kept), "kept": kept, "real_trade_allowed": False, "broker_order_allowed": False}
