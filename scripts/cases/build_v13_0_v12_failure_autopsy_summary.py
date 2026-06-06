#!/usr/bin/env python3
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    result={"status":"V13_0_V12_FAILURE_AUTOPSY_SUMMARY_BUILT","primary_failure_type":"CANDIDATE_FACTOR_DIRECTION_FAILED",
        "secondary_failure_types":["SUSPENSION_SAMPLE_CONTAMINATION_DETECTED_AND_REPAIRED","OLD_SEED_NO_LONGER_ELIGIBLE_FOR_NEXT_CYCLE"],
        "key_findings":["V12 seeds had 0/12 hit across two cycles","600837 was not a data gap but suspension/MA ineligible","after audited exclusion Cycle2 still missed 0/4","all T60 seeds downgraded to DO_NOT_PROMOTE"],
        "lessons_for_v13":["Universe eligibility must be checked before paper runs","Suspension/MA event samples must be filtered before bucket construction","Full ticker label coverage must be enforced","Failed seed reuse must be denied","New candidates must have new hypothesis and not reuse failed factor definitions"],
        "ready_for_new_candidate_design":True,"ready_for_alpha_claim":False,"alpha_validated":False,
        "production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    json.dump(result,open(C/"v13_0_v12_failure_autopsy_summary.json","w"),indent=2)
    print(f"Autopsy: BUILT")
if __name__=="__main__":main()
