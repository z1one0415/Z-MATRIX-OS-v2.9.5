#!/usr/bin/env python3
"""V12.4.6: Price Data Restore Full Chain."""
import subprocess,json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
S=["run_v12_4_5_label_regeneration_full_chain.py","build_v12_4_6_price_data_restore_contract.py",
   "check_v12_4_6_price_data_mount_gate.py","build_v12_4_6_label_provenance_template.py",
   "audit_v12_4_6_price_data_restore.py","build_v12_4_6_price_data_restore_closeout.py"]
def lo(p):return json.loads(p.read_text())if p.exists()else{}
def main():
    ok=True
    for s in S:
        r=subprocess.run(["python3",str(W/"scripts/cases"/s)],cwd=str(W),capture_output=True,text=True)
        print(f"{'OK'if r.returncode==0 else'FAIL'}: {s} {r.stdout.strip()[:120]}")
        if r.returncode!=0:print(f"  {r.stderr.strip()[:200]}");ok=False
    co=lo(C/"v12_4_6_price_data_restore_closeout.json");au=lo(C/"v12_4_6_price_data_restore_audit.json")
    final_ok=ok and"CONFIRMED"in co.get("status","")and"PASS"in au.get("status","")
    result={"status":"V12_4_6_PRICE_DATA_RESTORE_FULL_CHAIN_PASS"if final_ok else"V12_4_6_PRICE_DATA_RESTORE_FULL_CHAIN_BLOCKED",
        "steps":S,"steps_returncode_pass":ok,
        "price_data_currently_available":co.get("price_data_currently_available",False),
        "cycle2_still_blocked":True,"v12_5_still_blocked":True,
        "recommended_next_action":co.get("recommended_next_action",""),
        "investment_action_count":0,"trade_action_count":0,
        "ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v12_4_6_price_data_restore_full_chain.json","w"),indent=2)
    print(f"FullChain: {result['status']} | price={result['price_data_currently_available']}")
if __name__=="__main__":main()
