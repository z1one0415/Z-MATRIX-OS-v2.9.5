# allowlist: forbidden-token-definition
from __future__ import annotations
from statistics import mean
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY

def _ret(c,n):
    if len(c)<=n: return None
    prev=c[-n-1]; cur=c[-1]
    return (cur-prev)/prev*100 if prev else None

def _dd(c,n):
    if len(c)<n: return None
    h=max(c[-n:])
    return (c[-1]-h)/h*100 if h else None

def _vol(c,n):
    if len(c)<=n: return None
    rets=[]
    for i in range(max(1,len(c)-n),len(c)):
        if c[i-1]: rets.append(abs((c[i]-c[i-1])/c[i-1]*100))
    return mean(rets) if rets else None

def _bm(bm,dt,n):
    dates=sorted(bm); c=bm.get(dt)
    if c is None: return None
    idx=dates.index(dt)
    if idx<n: return None
    prev=bm[dates[idx-n]]
    return (c-prev)/prev*100 if prev else None

def build_sector_features(*, sector_indexes: dict, benchmark_bars=None) -> dict:
    bm = {x["trade_date"]:x["close"] for x in (benchmark_bars or [])}
    sf = {}
    for sector, rows in (sector_indexes or {}).items():
        rows=sorted(rows,key=lambda x:x["trade_date"]); out=[]
        for i,row in enumerate(rows):
            closes=[x["close_index"] for x in rows[:i+1]]; c0=closes[-1]
            f={"sector":sector,"trade_date":row["trade_date"],"close_index":c0,"sector_return_5d":_ret(closes,5),"sector_return_20d":_ret(closes,20),"sector_return_60d":_ret(closes,60),"sector_above_ma20":c0>mean(closes[-20:]) if len(closes)>=20 else None,"sector_above_ma60":c0>mean(closes[-60:]) if len(closes)>=60 else None,"sector_drawdown_from_20d_high":_dd(closes,20),"sector_volatility_20d":_vol(closes,20),"active_member_count":row.get("active_member_count"),"active_member_ratio":row.get("active_member_ratio"),"data_quality_status":row.get("data_quality_status"),"synthetic_sector_index":True,"uses_future_data":False}
            mr20=_bm(bm,row["trade_date"],20)
            f["sector_relative_strength_vs_market"]=f["sector_return_20d"]-mr20 if mr20 is not None and f["sector_return_20d"] is not None else None
            f["market_benchmark_status"]="READY" if mr20 is not None else "DATA_INSUFFICIENT"
            out.append(f)
        sf[sector]=out
    return {"feature_builder_version":"V3511_SECTOR_FEATURE_BUILDER_V10","sector_feature_count":len(sf),"sector_features":sf,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
