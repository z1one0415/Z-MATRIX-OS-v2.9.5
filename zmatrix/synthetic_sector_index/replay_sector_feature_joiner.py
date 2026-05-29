# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def join_replay_sector_features(*, replay_rows: list[dict], sector_mapping: dict, sector_features_with_phase: dict) -> dict:
    fm={}
    for sector,rows in (sector_features_with_phase or {}).items(): fm[sector]={r["trade_date"]:r for r in rows}
    joined=[]; ready=0
    for row in replay_rows or []:
        tk=str(row.get("ticker","")).split(".")[0].zfill(6); ed=str(row.get("entry_date") or row.get("replay_date","")).replace("-","")[:8]
        m=sector_mapping.get(tk,{}); s=m.get("sector"); f=fm.get(s,{}).get(ed)
        r2=dict(row); r2["sector"]=s; r2["sector_feature_join_status"]="MISSING"
        if f: r2.update({"sector_phase":f.get("sector_phase"),"sector_return_20d":f.get("sector_return_20d"),"sector_relative_strength_vs_market":f.get("sector_relative_strength_vs_market"),"sector_volatility_20d":f.get("sector_volatility_20d"),"synthetic_sector_index":True,"uses_future_data":False,"sector_feature_join_status":"READY"}); ready+=1
        joined.append(r2)
    t=len(replay_rows or []); cov=ready/t if t else 0
    return {"joiner_version":"V3511_REPLAY_SECTOR_FEATURE_JOINER_V10","replay_row_count":t,"join_ready_count":ready,"join_missing_count":t-ready,"join_coverage":cov,"join_status":"READY" if cov>=0.90 else "PARTIAL" if cov>0 else "DATA_INSUFFICIENT","joined_rows_sample":joined[:100],"joined_rows":joined,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
