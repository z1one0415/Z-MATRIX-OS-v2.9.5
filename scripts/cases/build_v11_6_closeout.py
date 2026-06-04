#!/usr/bin/env python3
"""V11.6 Closeout — reads OOS completion contract."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
ct=json.loads((C/"v11_6_1_oos_completion_contract.json").read_text())
tracking_done=ct.get("paper_tracking_period_completed",False)
co={"status":"V11_6_OOS_PAPER_TRACKING_FRAMEWORK_CONFIRMED","substage_confirmed":True,"substage_ready_for_v12_gate":tracking_done,"paper_tracking_period_completed":tracking_done,"global_ready_for_v12":tracking_done,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
json.dump(co,open(C/"v11_6_closeout.json","w"),indent=2)
print(f"V11.6 Closeout: tracking_completed={tracking_done}")
