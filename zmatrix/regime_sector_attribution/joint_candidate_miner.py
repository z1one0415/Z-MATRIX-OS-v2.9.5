from __future__ import annotations
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def mine_joint_candidates(*, joint_separability: dict) -> dict:
    status = joint_separability.get("joint_separability_status")
    candidates = []
    if status in ("JOINT_ATTRIBUTION_SEPARABLE","WEAKLY_JOINT_SEPARABLE"):
        for n in ["allow_b_rotation_in_bull_advance_sectors","block_b_rotation_in_bear_retreat_sectors","range_bound_only_in_advance_or_strong_sectors","sector_relative_strength_positive_only","exclude_sector_crash_and_retreat"]:
            candidates.append({"candidate_name":n,"lookahead_risk":False,"production_ready":False,"paper_replay_required":True,"uses_synthetic_sector_index":True,"synthetic_sector_index_production_allowed":False})
    return {"miner_version":"V3512_JOINT_CANDIDATE_MINER_V10","source_status":status,"candidate_count":len(candidates),"candidates":candidates,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
