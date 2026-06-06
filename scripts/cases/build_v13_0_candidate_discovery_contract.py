#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    ct=load("v13_0_research_restart_contract.json");dl=load("v13_0_failed_seed_denylist.json")
    us=load("v13_0_universe_eligibility_scan.json")
    ok=ct.get("v13_candidate_discovery_allowed",False)and us.get("universe_scan_ready_for_candidate_generation",False)
    result={"status":"V13_0_CANDIDATE_DISCOVERY_CONTRACT_BUILT"if ok else"V13_0_CANDIDATE_DISCOVERY_CONTRACT_BLOCKED",
        "discovery_mode":"NEW_HYPOTHESIS_ONLY","failed_seed_reuse_blocked":True,"universe_eligibility_required":True,
        "candidate_count_target":8,"candidate_count_min":4,
        "allowed_candidate_families":["CROSS_SECTIONAL_QUALITY_REVERSAL","FUNDAMENTAL_MOMENTUM_PROXY","LIQUIDITY_REGIME_INTERACTION","RELATIVE_STRENGTH_STABILITY","VOLATILITY_ADJUSTED_REVERSAL","INDUSTRY_NEUTRAL_RANK_INTERACTION"],
        "blocked_candidate_families":["RAW_AMOUNT_AVERAGE_REUSE","RAW_MOMENTUM_60D_REUSE","RAW_TRAILING_BENCHMARK_REUSE","RAW_VOLATILITY_REUSE"],
        "requires_new_hypothesis_id":True,"requires_factor_definition_hash":True,"requires_denylists_check":True,"requires_universe_gate":True,
        "ready_for_candidate_generation":ok,"ready_for_paper_bootstrap":False,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_candidate_discovery_contract.json","w"),indent=2)
    print(f"DiscoContract: {result['status']}")
if __name__=="__main__":main()
