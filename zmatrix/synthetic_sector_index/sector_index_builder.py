# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.synthetic_sector_index.schema import DEFAULT_SYNTHETIC_SECTOR_SAFETY, BASE_INDEX_VALUE

def build_synthetic_sector_indexes(*, sector_daily_returns: dict) -> dict:
    si = {}
    for sector, rows in (sector_daily_returns or {}).items():
        ci = BASE_INDEX_VALUE; out = []
        for row in sorted(rows, key=lambda x:x["trade_date"]):
            ret = row.get("sector_return_1d")
            if ret is not None and row.get("data_quality_status")!="INSUFFICIENT_MEMBERS": ci = ci*(1+ret/100)
            r2 = dict(row); r2["close_index"]=ci; r2["synthetic_sector_index"]=True; r2["production_index_allowed"]=False; out.append(r2)
        si[sector]=out
    return {"index_builder_version":"V3511_SYNTHETIC_SECTOR_INDEX_BUILDER_V10","sector_index_count":len(si),"sector_indexes":si,"synthetic_sector_index":True,"production_index_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SYNTHETIC_SECTOR_SAFETY)}
