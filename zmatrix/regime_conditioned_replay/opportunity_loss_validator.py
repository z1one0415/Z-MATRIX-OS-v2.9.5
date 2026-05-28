from __future__ import annotations

def _clean(xs):
    out=[]
    for x in xs:
        try:
            if x is not None: out.append(float(x))
        except: pass
    return out

def validate_opportunity_loss(*, rows: list[dict], policy_names: list[str]) -> dict:
    results = {}
    for pn in policy_names:
        downgraded = [r for r in rows or [] if r.get("regime_policy_action","KEEP") in ("BLOCK","OBSERVE_ONLY")]
        kept = [r for r in rows or [] if r.get("regime_policy_action","KEEP")=="KEEP"]
        dg_rets = _clean([r.get("actual_return_t20") for r in downgraded])
        dg_pos = [x for x in dg_rets if x>0]
        kept_rate = len(kept)/len(rows) if rows else 0
        if kept_rate < 0.20: status = "LOW_KEPT_RATE_BLOCKED"
        elif kept_rate < 0.60: status = "CONCENTRATED_POLICY_RISK"
        else: status = "SAMPLE_RETENTION_OK"
        results[pn] = {"downgraded_count":len(downgraded),"downgraded_positive_rate":len(dg_pos)/len(dg_rets) if dg_rets else None,"downgraded_total_return":sum(dg_rets) if dg_rets else 0,"kept_rate":kept_rate,"opportunity_loss_status":status}
    return {"opportunity_loss_version":"V357_OPPORTUNITY_LOSS_VALIDATION_V10","policy_results":results}
