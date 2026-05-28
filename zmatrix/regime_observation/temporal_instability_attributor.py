from __future__ import annotations
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def attribute_temporal_instability(*, anti_overfit_report: dict) -> dict:
    pv = anti_overfit_report.get("per_policy_validation",{}) or {}
    results = {}
    for pn, payload in pv.items():
        t = payload.get("temporal",{}) or {}; windows = t.get("windows",[]) or []
        passing = [w for w in windows if w.get("pass") is True]
        failing = [w for w in windows if w not in passing]
        reasons = []
        if len(windows) < 3: reasons.append("TEMPORAL_DATA_INSUFFICIENT")
        if len(passing) < 3: reasons.append("TEMPORAL_INSTABILITY_CONFIRMED")
        if t.get("temporal_status") == "TEMPORAL_INSTABILITY": reasons.append("UPSTREAM_TEMPORAL_BLOCKED")
        results[pn] = {"policy_name":pn,"window_count":len(windows),"passing_window_count":len(passing),"failing_window_count":len(failing),"best_windows":sorted(windows,key=lambda x:x.get("median_delta",0),reverse=True)[:5],"worst_windows":sorted(windows,key=lambda x:x.get("median_delta",0))[:5],"temporal_failure_reasons":reasons,"temporal_attribution_status":"TEMPORAL_INSTABILITY_CONFIRMED" if reasons else "TEMPORAL_STABLE","real_trade_allowed":False,"broker_order_allowed":False}
    return {"attribution_version":"V358_TEMPORAL_INSTABILITY_ATTRIBUTION_V10","policy_temporal_results":results,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
