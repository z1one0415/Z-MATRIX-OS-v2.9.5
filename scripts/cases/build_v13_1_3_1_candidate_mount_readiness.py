#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
CF={"INDUSTRY_NEUTRAL_REL_STRENGTH":["sector_or_industry"],"DOWNSIDE_VOL_ADJUSTED_STRENGTH":["drawdown_or_recovery"],"FUNDAMENTAL_MOMENTUM_PROXY":["fundamental_proxy_field"],"SECTOR_DISPERSION_REVERSAL":["sector_or_industry"],"DRAWDOWN_RECOVERY_QUALITY":["drawdown_or_recovery"],"TURNOVER_STABILITY_ANOMALY":["turnover"],"RELATIVE_RANK_ACCELERATION":["rank_short_medium"],"FUNDAMENTAL_QUALITY_STABILITY":["fundamental_proxy_field"]}
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    reg=load("v13_1_candidate_registry.json");md=load("v13_1_3_1_mount_decision.json")
    vd=set(d["feature_group"]for d in md.get("mount_decisions",[])if d.get("mount_decision")=="MOUNT_VALIDATED")
    items=[];ready=0;partial=0;blocked=0
    for r in reg.get("registry_items",[]):
        req=CF.get(r["factor_name"],[]);ok_req=[g for g in req if g in vd];bl=[g for g in req if g not in vd]
        if not bl:status="MOUNT_READY";ready+=1
        elif ok_req:status="MOUNT_PARTIAL";partial+=1
        else:status="MOUNT_BLOCKED";blocked+=1
        items.append({"v13_1_candidate_run_id":r["v13_1_candidate_run_id"],"factor_name":r["factor_name"],"required_feature_groups":req,"validated_feature_groups":ok_req,"blocked_feature_groups":bl,"candidate_mount_status":status,"ready_for_v13_1_4_materialization":status=="MOUNT_READY"})
    result={"status":"V13_1_3_1_CANDIDATE_MOUNT_READINESS_BUILT","candidate_count":len(items),"candidate_mount_ready_count":ready,"candidate_mount_partial_count":partial,"candidate_mount_blocked_count":blocked,"candidates":items,"ready_for_v13_1_4_materialization_candidate_count":ready,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_1_3_1_candidate_mount_readiness.json","w"),indent=2)
    print(f"Readiness: {ready}r/{partial}p/{blocked}b")
if __name__=="__main__":main()
