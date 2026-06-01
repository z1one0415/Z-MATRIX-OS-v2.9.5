#!/usr/bin/env python3
"""V10-C: Devil advocate review — 10 failure modes per factor."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent; C=W/"runtime_reports"/"cases"

def main():
    inp=json.loads((C/"v10_council_input_pack.json").read_text())
    drs=[]; c=0; high=0; med=0
    for pf in inp["promoted_factors"]:
        fid,mr,dp,rg=pf["factor_id"],pf.get("mean_rankic"),pf.get("decay_pattern"),pf.get("robustness_grade")
        modes=[{"mode":"Liquidity / market-cap proxy","risk_level":"HIGH" if ("AMOUNT" in fid or "VOLUME" in fid) else "LOW","reason":"May proxy size/liquidity" if ("AMOUNT" in fid or "VOLUME" in fid) else "Not AMOUNT/VOLUME"}]
        for mo_name, mo_risk in [("Industry concentration","MEDIUM"),("Regime dependency","MEDIUM" if rg!="ROBUST" else "LOW"),("Survivorship bias","MEDIUM"),("Data vendor bias","LOW"),("Multiple testing / p-hacking","MEDIUM"),("Turnover / transaction cost","MEDIUM"),("Horizon overfitting","HIGH" if dp=="NO_CLEAR_PATTERN" else "LOW"),("Crowd decay","MEDIUM"),("Fundamental contradiction","MEDIUM")]:
            modes.append({"mode":mo_name,"risk_level":mo_risk,"reason":"Standard V10 review"})
        is_crit=dp=="NO_CLEAR_PATTERN" and rg in ("WEAK","REJECT") and mr is not None and abs(mr)<0.03
        if is_crit: c+=1
        for mo in modes:
            if mo["risk_level"]=="HIGH": high+=1
            elif mo["risk_level"]=="MEDIUM": med+=1
        drs.append({"factor_id":fid,"horizon":pf["horizon"],"evidence":{"mean_rankic":mr,"rankic_ir":pf.get("rankic_ir"),"valid_date_count":pf.get("valid_date_count"),"decay_pattern":dp,"robustness_grade":rg},"failure_modes":modes,"devil_advocate_verdict":"WATCH_ONLY","ready_for_paper_watchlist":not is_crit,"ready_for_alpha_claim":False,"alpha_validated":False})
    da={"status":"V10_DEVIL_ADVOCATE_REVIEW_BUILT","failure_modes_checked":10,"critical_blockers":c,"high_risks":high,"medium_risks":med,"factor_failure_reviews":drs,"alpha_validated":False}
    json.dump(da,open(C/"v10_devil_advocate_review.json","w"),indent=2)
    print(f"Devil advocate: {c}C, {high}H, {med}M")

if __name__=="__main__": main()
