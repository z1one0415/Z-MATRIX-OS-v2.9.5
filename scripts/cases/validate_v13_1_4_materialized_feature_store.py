#!/usr/bin/env python3
"""V13.1.4 Validator — per-candidate feature value integrity check."""
import json,csv,io,os
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
NUMERIC=["fundamental_proxy_score","drawdown_depth_20d","recovery_slope_5d","downside_vol_20d","turnover","short_rank","medium_rank","rank_acceleration"]
FORBIDDEN=["forward_return","future_label","t20_return","t60_return","bucket_return","bucket_spread","hit_count","miss_count"]
CF={"INDUSTRY_NEUTRAL_REL_STRENGTH":["sector","industry"],"DOWNSIDE_VOL_ADJUSTED_STRENGTH":["drawdown_depth_20d","recovery_slope_5d","downside_vol_20d"],"FUNDAMENTAL_MOMENTUM_PROXY":["fundamental_proxy_score"],"SECTOR_DISPERSION_REVERSAL":["sector","industry"],"DRAWDOWN_RECOVERY_QUALITY":["drawdown_depth_20d","recovery_slope_5d"],"TURNOVER_STABILITY_ANOMALY":["turnover"],"RELATIVE_RANK_ACCELERATION":["short_rank","medium_rank","rank_acceleration"],"FUNDAMENTAL_QUALITY_STABILITY":["fundamental_proxy_score"]}
def load(n):p=C/n;return json.loads(p.read_text())if p.exists()else{}
def main():
    fd=os.environ.get("V13_FIXTURE_DIR","")
    pfx=Path(fd).name+"_"if fd else""
    manifest=load(f"fixtures/{pfx}feature_store_manifest.json")if fd else load("v13_1_4_materialized_feature_store_manifest.json")
    reasons=[]
    if manifest.get("status")!="V13_1_4_MATERIALIZED_FEATURE_STORE_BUILT":
        reasons.extend(manifest.get("blocked_reasons",["MATERIALIZATION_NOT_COMPLETED"]))
        out={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_BLOCKED","blocking_reasons":reasons,"per_candidate_validation_status":[],"candidate_ready_after_materialization_count":0}
    else:
        fpath=manifest.get("materialized_feature_store_path","")
        fp=W/fpath
        if not fp.exists():reasons.append("FILE_NOT_FOUND");out={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_BLOCKED","blocking_reasons":reasons}
        elif fp.stat().st_size==0:reasons.append("FILE_EMPTY");out={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_BLOCKED","blocking_reasons":reasons}
        else:
            rows=list(csv.DictReader(io.StringIO(fp.read_text())))
            cols=list(rows[0].keys())if rows else[]
            # Check forbidden fields
            for fb in FORBIDDEN:
                if any(fb in c.lower()for c in cols):reasons.append(f"FORBIDDEN_FIELD:{fb}")
            # Check 600837
            tkr_600837=[r for r in rows if r.get("ticker")=="600837"]
            if tkr_600837:reasons.append(f"TICKER_600837:{len(tkr_600837)}")
            # Check source_sha256 format
            for r in rows[:5]:
                sh=r.get("source_sha256","")
                if not sh or sh in("MULTIPLE","UNKNOWN",""):reasons.append(f"INVALID_SHA256:{sh}");break
                if len(sh)<16:reasons.append(f"SHORT_SHA256:{sh}");break
            # Per-candidate validation
            pc_status=[]
            rc=0
            for nm,req_cols in CF.items():
                miss_col=[c for c in req_cols if c not in cols]
                if miss_col:
                    pc_status.append({"factor_name":nm,"required_columns":req_cols,"covered_ticker_count":0,"missing_value_count":0,"numeric_parse_error_count":0,"coverage_ratio":0.0,"candidate_validation_status":"FEATURE_VALUES_BLOCKED","blocking_reasons":["MISSING_COLUMNS"]})
                    continue
                # Check values
                cov=0;miss=0;num_err=0;total=len(rows)
                for r in rows:
                    all_ok=True
                    for c in req_cols:
                        v=r.get(c,"")
                        if not v:miss+=1;all_ok=False;break
                        if c in NUMERIC:
                            try:float(v)
                            except:num_err+=1;all_ok=False;break
                    if all_ok:cov+=1
                cov_r=round(cov/total,4)if total>0 else 0
                if cov_r>=0.95 and miss==0 and num_err==0:
                    pc_status.append({"factor_name":nm,"required_columns":req_cols,"covered_ticker_count":cov,"missing_value_count":miss,"numeric_parse_error_count":num_err,"coverage_ratio":cov_r,"candidate_validation_status":"FEATURE_VALUES_VALIDATED","blocking_reasons":[]})
                    rc+=1
                else:
                    br=[]
                    if cov_r<0.95:br.append(f"COVERAGE_LOW:{cov_r}")
                    if miss>0:br.append(f"MISSING_VALUES:{miss}")
                    if num_err>0:br.append(f"NUMERIC_ERRORS:{num_err}")
                    pc_status.append({"factor_name":nm,"required_columns":req_cols,"covered_ticker_count":cov,"missing_value_count":miss,"numeric_parse_error_count":num_err,"coverage_ratio":cov_r,"candidate_validation_status":"FEATURE_VALUES_BLOCKED","blocking_reasons":br})
            if reasons:out={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_BLOCKED","blocking_reasons":reasons,"per_candidate_validation_status":pc_status,"candidate_ready_after_materialization_count":rc}
            else:out={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_VALIDATION_PASS","per_candidate_validation_status":pc_status,"candidate_ready_after_materialization_count":rc,"field_value_integrity_pass":True,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
    # Write output
    out_dir=C/"fixtures"if fd else C
    out_dir.mkdir(parents=True,exist_ok=True)
    op=out_dir/f"{pfx}feature_store_validation.json"
    json.dump(out,open(op,"w"),indent=2)
    print(f"Validate: {out.get('status','?')} ready={out.get('candidate_ready_after_materialization_count',0)}")
if __name__=="__main__":main()
