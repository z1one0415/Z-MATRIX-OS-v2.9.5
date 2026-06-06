#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    co=load("v12_5_multicycle_feedback_closeout.json");ledger=load("v12_5_cycle2_ledger_append.json")
    mem=load("v12_5_factor_memory_update.json")
    # Cycle1 factors from V12.3 memory
    cycle1_states={"AMOUNT_20D_AVG|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","AMOUNT_20D_AVG|T60":"WEAKENED_AFTER_SECOND_CYCLE",
                   "AMOUNT_60D_AVG|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","AMOUNT_60D_AVG|T60":"WEAKENED_AFTER_SECOND_CYCLE",
                   "MOM_60D|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","MOM_60D|T60":"WEAKENED_AFTER_SECOND_CYCLE",
                   "TRAILING_BENCHMARK_RELATIVE_60D|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","TRAILING_BENCHMARK_RELATIVE_60D|T60":"WEAKENED_AFTER_SECOND_CYCLE",
                   "VOLATILITY_20D|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","VOLATILITY_20D|T60":"WEAKENED_ON_FIRST_LIVE_CYCLE",
                   "VOLATILITY_60D|T20":"WEAKENED_ON_FIRST_LIVE_CYCLE","VOLATILITY_60D|T60":"WEAKENED_ON_FIRST_LIVE_CYCLE"}
    frozen=[]
    for k,state in cycle1_states.items():
        fid,hz=k.split("|")
        frozen.append({"factor_id":fid,"horizon":hz,"final_state":state,"reuse_allowed":False})
    result={"status":"V13_0_V12_FAILURE_FREEZE_MANIFEST_BUILT","freeze_scope":"V12_FAILED_RESEARCH_LOOP",
        "cycle_count":2,"total_evaluated_observations":12,"total_hit_count":0,"total_miss_count":12,
        "research_loop_outcome":"NO_ALPHA_FOUND","failed_seed_reuse_policy":"DENY_REUSE_UNLESS_REDESIGNED_AND_REJUSTIFIED",
        "v12_loop_closed":True,"frozen_factors":frozen,
        "ready_for_new_candidate_discovery":True,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_v12_failure_freeze_manifest.json","w"),indent=2)
    print(f"Freeze: {len(frozen)} factors frozen")
if __name__=="__main__":main()
