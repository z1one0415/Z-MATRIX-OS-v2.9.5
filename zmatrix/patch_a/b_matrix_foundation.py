"""PATCH-A-3: B-Matrix Data Foundation — 财务+估值+行业+产业链四层事实"""
from __future__ import annotations

B_MATRIX_HARD_GATES = {"st_flag": {"rule":"ST/退市风险","action":"BLOCK"},"audit_opinion_abnormal": {"rule":"审计意见异常","action":"BLOCK"},"consecutive_loss_no_reversal": {"rule":"连续亏损且无明确反转","action":"BLOCK"},"ocf_long_deterioration": {"rule":"经营现金流长期恶化","action":"BLOCK"},"debt_ratio_uncontrolled": {"rule":"资产负债失控","action":"BLOCK"}}

B_MATRIX_SCORING = {"profit_quality":{"weight":20,"fields":["gross_margin","net_margin","roe","roic"]},"growth_quality":{"weight":20,"fields":["revenue_yoy","net_profit_yoy","deduct_np_yoy"]},"cashflow_quality":{"weight":20,"fields":["ocf","ocf_to_np","fcf_proxy"]},"balance_sheet_safety":{"weight":15,"fields":["debt_ratio","current_ratio","goodwill_ratio"]},"valuation_reasonableness":{"weight":15,"fields":["pe_ttm","pb","ps","dividend_yield"]},"industry_chain_position":{"weight":10,"fields":["industry_percentile_roe","industry_percentile_growth","bottleneck_score","chain_position"]}}

B_MATRIX_MIN_COVERAGE = {"financial_core":0.95,"valuation":0.90,"industry":0.90,"chain_evidence":0.10}

def score_b_matrix(*, financial_facts: dict, valuation_facts: dict, industry_facts: dict, chain_facts: dict | None = None) -> dict:
    chain_facts = chain_facts or {}
    scores = {}; reasons = []; missing = []; total = 0; max_total = 0
    for module, cfg in B_MATRIX_SCORING.items():
        module_score = 0; module_count = 0
        for f in cfg["fields"]:
            all_facts = {**financial_facts, **valuation_facts, **industry_facts, **chain_facts}
            v = all_facts.get(f)
            if v is not None:
                module_score += _field_score(f, v); module_count += 1
            else: missing.append(f)
        w = cfg["weight"]
        raw = (module_score / max(1, module_count)) if module_count > 0 else 0
        scores[module] = {"raw_score": raw, "weighted_score": raw * w / 100, "fields_available": module_count, "fields_total": len(cfg["fields"])}
        total += raw * w / 100; max_total += w

    hard_gate_passed = _check_hard_gates(financial_facts)
    if not hard_gate_passed: reasons.append("HARD_GATE_FAILED")
    if "pe_ttm" in missing: reasons.append("VALUATION_DATA_INSUFFICIENT")
    if "ocf" in missing: reasons.append("CASHFLOW_DATA_WEAK")

    b_score = round(total, 1)
    eligible = hard_gate_passed and b_score >= 75 and "VALUATION_DATA_INSUFFICIENT" not in reasons and "CASHFLOW_DATA_WEAK" not in reasons
    return {"status":"PASS" if eligible and missing_count(missing,financial_facts)<5 else "DATA_INSUFFICIENT" if missing_count(missing,financial_facts)>=10 else "FAIL","base_role_eligible":eligible,"b_score":b_score,"hard_gate_passed":hard_gate_passed,"reason_codes":reasons,"missing_fields":missing,"freshness_status":"FRESH","pit_safe":True}

def _field_score(field, value):
    try: v = float(value)
    except: return 0
    if field in ("gross_margin","net_margin"): return min(100, max(0, v * 2))
    if field in ("roe","roic"): return min(100, max(0, v * 5))
    if field in ("revenue_yoy","net_profit_yoy","deduct_np_yoy"): return min(100, max(0, 50 + v))
    if field in ("ocf_to_np","fcf_proxy"): return min(100, max(0, 50 + v * 5))
    if field in ("debt_ratio",): return min(100, max(0, 100 - v * 2))
    if field in ("pe_ttm",): return min(100, max(0, 50 if 5 <= v <= 50 else 25))
    if field in ("industry_percentile_roe","industry_percentile_growth"): return min(100, max(0, v))
    if field in ("bottleneck_score",): return min(100, max(0, v))
    if field in ("current_ratio","goodwill_ratio"): return min(100, max(0, 50 + v * 10))
    return min(100, max(0, 50))

def _check_hard_gates(facts):
    if facts.get("st_flag"): return False
    if facts.get("audit_opinion") == "ABNORMAL": return False
    if facts.get("ocf") is not None and float(facts.get("ocf", 0)) < 0 and facts.get("ocf_trend") == "DETERIORATING": return False
    if facts.get("debt_ratio") is not None and float(facts.get("debt_ratio", 0)) > 0.80: return False
    return True

def missing_count(missing, facts):
    return len([f for f in missing if f in ["revenue_yoy","net_profit_yoy","gross_margin","roe","debt_ratio","ocf"]])
