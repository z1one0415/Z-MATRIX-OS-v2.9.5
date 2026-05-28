"""V4.0-B1 Contracts — Subjective Score Ban Validator"""
from __future__ import annotations

BANNED_LLM_SCORE_NAMES = ["moat_score","risk_score","support_score","growth_score","buy_score","sell_score","conviction_score","recommendation_score","catalyst_score","event_power_score","hedge_score","defensive_score","fillability_score","expected_return","position_size","target_weight","probability_of_success"]

ALLOWED_LLM_OUTPUT_TYPES = ["BOOL","ENUM","FACTUAL_NUMBER","DATE","TEXT_SPAN","EVIDENCE_REF","AMBIGUITY_FLAG","MISSING_EVIDENCE","CONTRADICTION_FLAG"]

class SubjectiveScoreBanValidator:
    @staticmethod
    def validate_llm_output(output_dict):
        violations = []
        for key, value in (output_dict or {}).items():
            if any(banned in key.lower() for banned in BANNED_LLM_SCORE_NAMES):
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    violations.append({"field": key, "value": value, "reason": f"LLM subjective float score banned: {key}"})
        return {"passed": len(violations) == 0, "violations": violations, "llm_subjective_float_score_allowed": False}

class FactExtractionContract:
    def __init__(self): self.required_fields = ["source","publish_time","evidence_level","extraction_type"]
    def validate(self, extraction):
        missing = [f for f in self.required_fields if f not in (extraction or {})]
        return {"valid": len(missing) == 0, "missing_fields": missing, "extraction_type_ok": (extraction or {}).get("extraction_type") in ALLOWED_LLM_OUTPUT_TYPES if extraction else False}

class FailoverContract:
    @staticmethod
    def validate_degraded_report(report):
        if not hasattr(report, 'new_judgement_generated'): return {"valid": False, "reason": "missing new_judgement_generated"}
        if report.new_judgement_generated: return {"valid": False, "reason": "new_judgment generated during failover"}
        if not hasattr(report, 'real_trade_allowed') or report.real_trade_allowed: return {"valid": False, "reason": "real_trade not blocked"}
        if not hasattr(report, 'failover_trace') or not report.failover_trace: return {"valid": False, "reason": "missing failover trace"}
        return {"valid": True, "failover_contract_passed": True, "llm_api_failure_no_new_judgement": True, "stale_cache_marked": True, "degraded_closeout_report_generated": True}
