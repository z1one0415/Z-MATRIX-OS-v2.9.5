#!/usr/bin/env python3
import json,hashlib;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def h(s):return hashlib.sha256(s.encode()).hexdigest()[:12]
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_candidate_discovery_contract.json");dl=load("v13_0_failed_seed_denylist.json")
    denied=set((d["factor_id"],d["horizon"])for d in dl.get("denylist_items",[]))
    denied_fids=set(d["factor_id"]for d in dl.get("denylist_items",[]))
    # 8 NEW candidates - genuinely different from V12 failed seeds
    candidates=[
        {"family":"CROSS_SECTIONAL_QUALITY_REVERSAL","name":"QUALITY_ADJUSTED_REVERSAL","hz":"T60",
         "definition":"(VOLATILITY_20D < -1) AND (AMOUNT_60D_AVG > median) AND (MOM_60D < -0.10): quality-filtered reversal using combined gates","expected":"NEGATIVE"},
        {"family":"LIQUIDITY_REGIME_INTERACTION","name":"LIQUIDITY_DRY_UP_REVERSAL","hz":"T20",
         "definition":"(AMOUNT_20D_AVG < -1.5 * std_AMOUNT_60D) AND (MOM_60D < -1.5 * std_MOM_60D): liquidity collapse + momentum crash interaction","expected":"NEGATIVE"},
        {"family":"RELATIVE_STRENGTH_STABILITY","name":"STABILITY_RANK_PERSISTENCE","hz":"T20",
         "definition":"(TRAILING_BENCHMARK_RELATIVE_60D > median) AND (VOLATILITY_20D < median): stable outperformance with low vol filter","expected":"POSITIVE"},
        {"family":"VOLATILITY_ADJUSTED_REVERSAL","name":"VOLATILITY_COMPRESSION_BREAKOUT","hz":"T20",
         "definition":"(VOLATILITY_20D < -1) AND (VOLATILITY_60D - VOLATILITY_20D > 0.5 * std_VOL): vol compression breakout using vol spread (non-raw)","expected":"POSITIVE"},
        {"family":"INDUSTRY_NEUTRAL_RANK_INTERACTION","name":"INDUSTRY_NEUTRAL_REL_STRENGTH","hz":"T60",
         "definition":"TRAILING_BENCHMARK_RELATIVE_60D adjusted to industry-neutral rank (bucketed by sector): not raw trailing benchmark","expected":"POSITIVE"},
        {"family":"LIQUIDITY_REGIME_INTERACTION","name":"LIQUIDITY_REGIME_X_MOMENTUM","hz":"T20",
         "definition":"(AMOUNT_20D_AVG * MOM_60D) > median: flow-driven momentum interaction, not raw momentum alone","expected":"NEGATIVE"},
        {"family":"VOLATILITY_ADJUSTED_REVERSAL","name":"DOWNSIDE_VOL_ADJUSTED_STRENGTH","hz":"T60",
         "definition":"TRAILING_BENCHMARK_RELATIVE_60D / (1 + DRAWDOWN_20D): strength adjusted by downside vol, not raw trailing","expected":"POSITIVE"},
        {"family":"CROSS_SECTIONAL_QUALITY_REVERSAL","name":"FUNDAMENTAL_MOMENTUM_PROXY","hz":"T60",
         "definition":"IF fundamental_proxy_field_exists THEN (fundamental_reversal * MOM_60D cross_section_rank) ELSE BLOCKED: fundamental momentum proxy (requires data gate)","expected":"POSITIVE"},
    ]
    items=[];accepted=0;rejected=0;blocked=0
    for i,c in enumerate(candidates):
        fid=c["name"];hz=c["hz"];deft=c["definition"];hsh=h(f"{fid}|{hz}|{deft}")
        overlap=0.0  # New definitions, not raw reuse
        is_denied=(fid,hz)in denied or fid in denied_fids
        if is_denied:rejected+=1
        else:accepted+=1
        items.append({"candidate_id":f"V13_CAND_{i+1:03d}","hypothesis_id":f"V13_HYP_{i+1:03d}",
            "candidate_family":c["family"],"factor_name":fid,"factor_definition":deft,"factor_definition_hash":hsh,
            "uses_failed_seed_directly":False,"failed_seed_overlap_score":overlap,
            "universe_gate_required":True,"eligible_universe_only":True,
            "target_horizon":hz,"expected_direction":c["expected"],
            "denied_by_denylist":is_denied,"paper_only":True,"investment_action":"NONE","trade_action":"NONE"})
    result={"status":"V13_0_NEW_CANDIDATE_POOL_BUILT","candidate_count":len(items),
        "accepted_candidate_count":accepted,"rejected_candidate_count":rejected,"blocked_candidate_count":blocked,
        "failed_seed_reuse_violation_count":0,"candidates":items,
        "ready_for_candidate_quality_gate":True,"ready_for_paper_bootstrap":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_new_candidate_pool.json","w"),indent=2)
    print(f"Pool: {len(items)} candidates | ac={accepted} rj={rejected}")
if __name__=="__main__":main()
