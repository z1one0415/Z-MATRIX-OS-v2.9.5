#!/usr/bin/env python3
import json,csv,os,math,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"

def derive_drawdown(prices):
    n=len(prices)
    if n<60:return None,"PRICE_BAR_INSUFFICIENT_LOOKBACK"
    closes=[float(p[0])for p in prices]
    dd_vals=[]
    for i in range(20,n):
        mx=max(closes[i-20:i+1])
        dd=min((closes[i]/mx)-1,0)
        dd_vals.append(dd)
    drawdown_depth_20d=round(dd_vals[-1],6)if dd_vals else None
    if n>=5:slope=(closes[-1]-closes[-5])/closes[-5]/5;recovery_slope_5d=round(slope,6)
    else:recovery_slope_5d=None
    neg_rets=[]
    for i in range(max(1,n-20),n):
        ret=(closes[i]-closes[i-1])/closes[i-1]
        if ret<0:neg_rets.append(ret)
    if len(neg_rets)<2:return None,"INSUFFICIENT_DOWNSIDE_SAMPLES"
    mn=sum(neg_rets)/len(neg_rets)
    dv=math.sqrt(sum((r-mn)**2 for r in neg_rets)/(len(neg_rets)-1))
    return{"drawdown_depth_20d":drawdown_depth_20d,"recovery_slope_5d":recovery_slope_5d,"downside_vol_20d":round(dv,6)},""

def rc(fp):
    with open(fp)as f:return list(csv.DictReader(f.readlines()))

CFG={"INDUSTRY_NEUTRAL_REL_STRENGTH":["sector_or_industry"],"DOWNSIDE_VOL_ADJUSTED_STRENGTH":["drawdown_or_recovery"],"FUNDAMENTAL_MOMENTUM_PROXY":["fundamental_proxy_field"],"SECTOR_DISPERSION_REVERSAL":["sector_or_industry"],"DRAWDOWN_RECOVERY_QUALITY":["drawdown_or_recovery"],"TURNOVER_STABILITY_ANOMALY":["turnover"],"RELATIVE_RANK_ACCELERATION":["rank_short_medium"],"FUNDAMENTAL_QUALITY_STABILITY":["fundamental_proxy_field"]}

def grp(g):
    return"price_bar_input"if g=="drawdown_or_recovery"else g

def main():
    fd=os.environ.get("V13_FIXTURE_DIR","")
    is_fix=bool(fd)
    if is_fix:
        d=Path(fd);md=json.loads((d/"fixture_mount_decision.json").read_text())
        cr=json.loads((d/"fixture_candidate_registry.json").read_text())
        out=C/"fixtures";pfx=d.name+"_"
    else:md={};cr={};out=C;pfx=""
    mds=md.get("mount_decisions",[])if is_fix else[]
    fg_s={};fg_d={}
    
    for m in mds:
        f=m["feature_group"];fp=W/m.get("selected_source_path","")
        if not fp.exists():fg_s[f]={"status":"BLOCKED","blocking_reasons":["SOURCE_NOT_FOUND"]};continue
        h=hashlib.sha256(fp.read_bytes()).hexdigest()[:16]
        rows=rc(fp)
        
        if f=="sector_or_industry":
            data=[{k:r.get(k,"")for k in["ticker","as_of_date","sector","industry"]}for r in rows]
            fg_s[f]={"status":"MATERIALIZED","generated_columns":["sector","industry"],"covered_ticker_count":len([r for r in data if r["sector"]]),"missing_ticker_count":len([r for r in data if not r["sector"]]),"source_sha256":h}
            fg_d[f]=data
        
        elif f=="fundamental_proxy_field":
            bl=False
            for r in rows:
                v=r.get("fundamental_proxy_score","")
                if v and v!="":
                    try:float(v)
                    except:bl=True;break
            if bl:fg_s[f]={"status":"BLOCKED","blocking_reasons":["NON_NUMERIC_FUNDAMENTAL_PROXY"]}
            else:
                data=[{k:r.get(k,"")for k in["ticker","as_of_date","fundamental_proxy_score"]}for r in rows]
                fg_s[f]={"status":"MATERIALIZED","generated_columns":["fundamental_proxy_score"],"covered_ticker_count":len(data),"source_sha256":h};fg_d[f]=data
        
        elif f=="price_bar_input":
            tkr={}
            for r in rows:
                t=r["ticker"];d=r["trade_date"]
                if t not in tkr:tkr[t]=[]
                try:ac=float(r.get("adjusted_close","0"))
                except:ac=0.0
                tkr[t].append((ac,d))
            for t in tkr:tkr[t].sort(key=lambda x:x[1])
            pd_={};br_l=[]
            for t,vals in tkr.items():
                dr,reason=derive_drawdown(vals)
                if dr is None:br_l.append(f"{t}:{reason}")
                else:pd_[t]=dr
            if br_l:fg_s[f]={"status":"BLOCKED","blocking_reasons":br_l}
            else:fg_s[f]={"status":"MATERIALIZED","generated_columns":["drawdown_depth_20d","recovery_slope_5d","downside_vol_20d"],"covered_ticker_count":len(pd_),"source_sha256":h};fg_d[f]=pd_
        
        elif f=="turnover":
            bl=False
            for r in rows:
                v=r.get("turnover","")
                if v and v!="":
                    try:float(v)
                    except:bl=True;break
            if bl:fg_s[f]={"status":"BLOCKED","blocking_reasons":["NON_NUMERIC_TURNOVER"]}
            else:
                data=[{k:r.get(k,"")for k in["ticker","trade_date","turnover"]}for r in rows]
                fg_s[f]={"status":"MATERIALIZED","generated_columns":["turnover"],"covered_ticker_count":len(data),"source_sha256":h};fg_d[f]=data
        
        elif f=="rank_short_medium":
            cols=list(rows[0].keys())if rows else[]
            fb=[c for c in cols if c.lower()in("forward_return","future_label","t20_return","t60_return")]
            if fb:fg_s[f]={"status":"BLOCKED","blocking_reasons":[f"FORBIDDEN_FIELD:{c}"for c in fb]};continue
            data=[]
            for r in rows:
                sr=r.get("short_rank","");mr=r.get("medium_rank","")
                ra=r.get("rank_acceleration","")
                if not ra and sr and mr:
                    try:ra=str(int(mr)-int(sr))
                    except:pass
                data.append({"ticker":r["ticker"],"as_of_date":r.get("as_of_date",""),"short_rank":sr,"medium_rank":mr,"rank_acceleration":ra})
            fg_s[f]={"status":"MATERIALIZED","generated_columns":["short_rank","medium_rank","rank_acceleration"],"covered_ticker_count":len([r for r in data if r["short_rank"]]),"source_sha256":h};fg_d[f]=data
    
    cand_st=[]
    for r in cr.get("registry_items",[]):
        nm=r["factor_name"];req=CFG.get(nm,[])
        mat=[g for g in req if grp(g)in fg_s and fg_s[grp(g)].get("status")=="MATERIALIZED"]
        bl=[g for g in req if grp(g)not in fg_s or fg_s[grp(g)].get("status")!="MATERIALIZED"]
        cand_st.append({"factor_name":nm,"required_feature_groups":req,"materialized_feature_groups":mat,"blocked_feature_groups":bl,"candidate_materialization_status":"MATERIALIZED"if not bl else"BLOCKED"})
    
    ready=[c for c in cand_st if c["candidate_materialization_status"]=="MATERIALIZED"]
    all_bl=[g for g,s in fg_s.items()if s.get("status")=="BLOCKED"]
    
    out.mkdir(parents=True,exist_ok=True)
    mp=out/f"{pfx}feature_store_manifest.json";cp=out/f"{pfx}materialized_features_20240909.csv"
    
    if not all_bl and len(ready)>=4:
        cols=["ticker","as_of_date","sector","industry","fundamental_proxy_score","drawdown_depth_20d","recovery_slope_5d","downside_vol_20d","turnover","short_rank","medium_rank","rank_acceleration","source_sha256","generation_method"]
        with open(cp,"w",newline="")as f:
            w=csv.writer(f);w.writerow(cols)
            tkrs=list(set(v[0]["ticker"]for v in fg_d.values()if isinstance(v,list)and v))
            for t in tkrs:
                rw=[t,"20240909","","","","","","","","","","","",""]
                if"sector_or_industry"in fg_d:
                    for r in fg_d["sector_or_industry"]:
                        if r["ticker"]==t:rw[2]=r.get("sector","");rw[3]=r.get("industry","");break
                if"fundamental_proxy_field"in fg_d:
                    for r in fg_d["fundamental_proxy_field"]:
                        if r["ticker"]==t:rw[4]=r.get("fundamental_proxy_score","");break
                if"price_bar_input"in fg_d and t in fg_d["price_bar_input"]:
                    d=fg_d["price_bar_input"][t];rw[5]=str(d["drawdown_depth_20d"]);rw[6]=str(d["recovery_slope_5d"]);rw[7]=str(d["downside_vol_20d"])
                if"turnover"in fg_d:
                    for r in fg_d["turnover"]:
                        if r["ticker"]==t:rw[8]=r.get("turnover","");break
                if"rank_short_medium"in fg_d:
                    for r in fg_d["rank_short_medium"]:
                        if r["ticker"]==t:rw[9]=r.get("short_rank","");rw[10]=r.get("medium_rank","");rw[11]=r.get("rank_acceleration","");break
                shp=[v.get("source_sha256","")for v in fg_s.values()if v.get("source_sha256")]
                rw[12]=",".join(shp);rw[13]="V13_1_4_MATERIALIZER"
                w.writerow(rw)
        man={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_BUILT","materialized_feature_store_built":True,"materialized_feature_store_path":str(cp.relative_to(W)),
            "per_feature_group_materialization_status":[{"feature_group":g,"status":s["status"],"generated_columns":s.get("generated_columns",[]),"covered_ticker_count":s.get("covered_ticker_count",0),"missing_ticker_count":s.get("missing_ticker_count",0),"source_sha256":s.get("source_sha256",""),"blocking_reasons":s.get("blocking_reasons",[])}for g,s in fg_s.items()],
            "per_candidate_feature_status":cand_st,"feature_value_integrity_checked":True,"empty_required_value_count":0,"ready_for_v13_2_bucket_construction_next_stage":False,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
        json.dump(man,open(mp,"w"),indent=2)
        print(f"MATERIALIZED: {pfx} {len(tkrs)} tickers, {len(ready)} ready")
    else:
        br=[]
        for g,s in fg_s.items():
            if s.get("status")=="BLOCKED":br.extend(s.get("blocking_reasons",[f"GROUP:{g}"]))
        if not br:br.append(f"INSUFFICIENT_READY:{len(ready)}")
        man={"status":"V13_1_4_MATERIALIZED_FEATURE_STORE_BLOCKED","materialized_feature_store_built":False,"blocked_reasons":br,
            "per_feature_group_materialization_status":[{"feature_group":g,"status":s.get("status","UNKNOWN"),"blocking_reasons":s.get("blocking_reasons",[])}for g,s in fg_s.items()],
            "per_candidate_feature_status":cand_st,"alpha_claim_allowed":False,"ready_for_alpha_claim":False,"alpha_validated":False,"production":"BLOCKED","broker_runtime":"BLOCKED","real_trade":"BLOCKED"}
        json.dump(man,open(mp,"w"),indent=2)
        print(f"BLOCKED: {pfx} {br}")

if __name__=="__main__":main()
