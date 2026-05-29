# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_conditioned_replay.temporal_split_validator import validate_temporal_stability
from zmatrix.regime_conditioned_replay.sector_split_validator import validate_sector_stability
from zmatrix.regime_conditioned_replay.stress_window_validator import validate_stress_windows
from zmatrix.regime_conditioned_replay.opportunity_loss_validator import validate_opportunity_loss
from zmatrix.regime_conditioned_replay.stability_verdict import build_stability_verdict
from zmatrix.regime_conditioned_replay.anti_overfit_schema import DEFAULT_ANTI_OVERFIT_SAFETY

def build_anti_overfit_report(*, rows: list[dict], full_sample_policies: list[str]) -> dict:
    temporal = validate_temporal_stability(rows=rows, policy_names=full_sample_policies)
    sector = validate_sector_stability(rows=rows, policy_names=full_sample_policies)
    stress = validate_stress_windows(rows=rows, policy_names=full_sample_policies)
    opportunity = validate_opportunity_loss(rows=rows, policy_names=full_sample_policies)
    verdict = build_stability_verdict(full_sample_policies=full_sample_policies, temporal=temporal, sector=sector, stress=stress, opportunity=opportunity)
    return {"report_version":"V357_ANTI_OVERFIT_VALIDATION_REPORT_V10","mode":"ANTI_OVERFIT_VALIDATION_ONLY","full_sample_pass_policies":full_sample_policies,"temporal_validation":temporal,"sector_validation":sector,"stress_validation":stress,"opportunity_loss_validation":opportunity,"stability_verdict":verdict,"final_promoted_policies":verdict.get("promoted_policies",[]),"recommended_next_step":verdict.get("verdicts",{}).get(full_sample_policies[0],{}).get("recommended_next_step","v3.5.8") if full_sample_policies else "v3.5.8","production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"runtime_enabled":False,"safety":dict(DEFAULT_ANTI_OVERFIT_SAFETY)}
