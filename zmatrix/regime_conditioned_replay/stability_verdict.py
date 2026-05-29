# allowlist: forbidden-token-definition
from __future__ import annotations

def build_stability_verdict(*, full_sample_policies: list[str], temporal: dict, sector: dict, stress: dict, opportunity: dict) -> dict:
    verdicts = {}
    for pn in full_sample_policies:
        reasons = []
        t = temporal.get("policy_results",{}).get(pn,{})
        s = sector.get("policy_results",{}).get(pn,{})
        st = stress.get("policy_results",{}).get(pn,{})
        op = opportunity.get("policy_results",{}).get(pn,{})

        if op.get("opportunity_loss_status") == "LOW_KEPT_RATE_BLOCKED": reasons.append("KEPT_RATE_TOO_LOW")
        elif op.get("opportunity_loss_status") == "CONCENTRATED_POLICY_RISK": reasons.append("CONCENTRATED_POLICY_RISK")

        if t.get("temporal_status") == "TEMPORAL_INSTABILITY": reasons.append("TEMPORAL_INSTABILITY")
        elif t.get("temporal_status") == "INSUFFICIENT_WINDOWS": reasons.append("INSUFFICIENT_TEMPORAL_WINDOWS")

        if s.get("sector_status") == "SECTOR_INSTABILITY": reasons.append("SECTOR_INSTABILITY")

        if reasons:
            if "KEPT_RATE_TOO_LOW" in reasons: status = "LOW_KEPT_RATE_BLOCKED"
            elif "TEMPORAL_INSTABILITY" in reasons: status = "TEMPORAL_INSTABILITY_BLOCKED"
            else: status = "OVERFIT_RISK_BLOCKED"
        elif s.get("sector_status") == "DATA_INSUFFICIENT": status = "STABILITY_WEAK_OBSERVATION_ONLY"
        else: status = "STABILITY_VALIDATED_OBSERVATION_READY"

        promotion = status == "STABILITY_VALIDATED_OBSERVATION_READY"
        next_step = {"STABILITY_VALIDATED_OBSERVATION_READY":"v3.5.8 Regime Policy Observation Portfolio Simulation","STABILITY_WEAK_OBSERVATION_ONLY":"v3.5.8 Regime Observation + Sector Data Enrichment","OVERFIT_RISK_BLOCKED":"v3.5.8 B-Matrix Reconstruction","LOW_KEPT_RATE_BLOCKED":"v3.5.8 Capacity Study","TEMPORAL_INSTABILITY_BLOCKED":"v3.5.8 Temporal Robustness Repair"}.get(status,"v3.5.8")

        verdicts[pn] = {"anti_overfit_status":status,"reasons":reasons,"promotion_allowed":promotion,"recommended_next_step":next_step}

    promoted = [pn for pn,v in verdicts.items() if v["promotion_allowed"]]
    return {"stability_verdict_version":"V357_STABILITY_VERDICT_V10","verdicts":verdicts,"promoted_policies":promoted,"real_trade_allowed":False,"broker_order_allowed":False}
