#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:12]
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_2_candidate_redesign_contract.json");ar=load("v13_0_2_rejected_candidate_archive.json")
    pool=load("v13_0_new_candidate_pool.json");sc=load("v13_0_1_candidate_overlap_scorecard.json")
    sc_map={s["candidate_id"]:s for s in sc.get("scorecards",[])}
    # Keep only PASS_OVERLAP_GATE candidates
    preserved=[]
    for c in pool.get("candidates",[]):
        s=sc_map.get(c["candidate_id"],{})
        if s.get("overlap_decision")=="PASS_OVERLAP_GATE":
            preserved.append(c)
    # 6 NEW low-overlap candidates
    new_candidates=[
        {"family":"INDUSTRY_NEUTRAL_RANK_INTERACTION","name":"SECTOR_DISPERSION_REVERSAL","hz":"T20",
         "definition":"sector_dispersion_zscore + within_sector_reversal_rank: sector structure, no raw V12 factor dependency","expected":"POSITIVE"},
        {"family":"DOWNSIDE_RISK_RECOVERY","name":"DRAWDOWN_RECOVERY_QUALITY","hz":"T20",
         "definition":"drawdown_depth_20d AND recovery_slope_5d interaction: downside/recovery structure","expected":"POSITIVE"},
        {"family":"LIQUIDITY_STRUCTURE_STABILITY","name":"TURNOVER_STABILITY_ANOMALY","hz":"T20",
         "definition":"turnover_stability_score over 20d with abnormal turnover shock filter: liquidity structure","expected":"POSITIVE"},
        {"family":"RANK_DYNAMICS","name":"RELATIVE_RANK_ACCELERATION","hz":"T20",
         "definition":"rank_acceleration_diff between short_rank and medium_rank: rank dynamics, no raw momentum","expected":"POSITIVE"},
        {"family":"FUNDAMENTAL_MOMENTUM_PROXY","name":"FUNDAMENTAL_QUALITY_STABILITY","hz":"T60",
         "definition":"quality_stability_proxy from fundamental fields: no raw price momentum dependency","expected":"POSITIVE"},
        {"family":"EVENT_CLEAN_STRENGTH","name":"EVENT_CLEAN_REL_STRENGTH","hz":"T60",
         "definition":"relative_strength after excluding suspension/MA/delisting contaminated names: event-clean universe","expected":"POSITIVE"},
    ]
    items=[]
    for c in preserved:
        items.append({**c,"overlap_status":"PRESERVED_PASSED_V13_0_1"})
    for i,c in enumerate(new_candidates):
        fid=c["name"];hz=c["hz"];deft=c["definition"];hsh=h(f"{fid}|{hz}|{deft}")
        items.append({"candidate_id":f"V13_CAND_{i+9:03d}","hypothesis_id":f"V13_HYP_{i+9:03d}",
            "candidate_family":c["family"],"factor_name":fid,"factor_definition":deft,"factor_definition_hash":hsh,
            "uses_failed_seed_directly":False,"failed_seed_overlap_score":None,
            "overlap_scoring_required":True,"overlap_scoring_source":"V13_0_2_OVERLAP_RESCORE_REQUIRED",
            "is_new_candidate":True,"universe_gate_required":True,"eligible_universe_only":True,
            "target_horizon":hz,"expected_direction":c["expected"],
            "paper_only":True,"investment_action":"NONE","trade_action":"NONE"})
    result={"status":"V13_0_2_REDESIGNED_CANDIDATE_POOL_BUILT","candidate_count":len(items),
        "preserved_candidate_count":len(preserved),"new_candidate_count":len(new_candidates),
        "archived_rejected_candidate_count":ar.get("rejected_count",5),"candidates":items,
        "ready_for_overlap_rescoring":True,"ready_for_v13_1_paper_bootstrap":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_2_redesigned_candidate_pool.json","w"),indent=2)
    print(f"Pool: {len(items)} total ({len(preserved)} preserved + {len(new_candidates)} new)")
if __name__=="__main__":main()
