from __future__ import annotations
import csv, json
from pathlib import Path
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY, TICKER_FIELDS, NAME_FIELDS, SECTOR_FIELDS, THEME_FIELDS, MARKET_FIELDS, LIST_DATE_FIELDS

def _first(row,fs):
    for f in fs:
        if row.get(f) not in (None,""): return row[f],f
    return None,None

def _norm_t(x):
    if x in (None,""): return None
    s = str(x).strip()
    if "." in s: return s.split(".")[0].zfill(6)
    if s.isdigit(): return s.zfill(6)
    return s[:6] if len(s)>=6 else s

def normalize_mapping_sources(*, source_files: list[str]) -> dict:
    rows = []
    for f in (source_files or []):
        p = Path(f)
        if not p.exists(): continue
        raw = list(csv.DictReader(open(p,encoding="utf-8-sig"))) if p.suffix==".csv" else _load_json(p) if p.suffix==".json" else []
        for r in raw:
            t,_ = _first(r, TICKER_FIELDS); n,_ = _first(r, NAME_FIELDS); s,_ = _first(r, SECTOR_FIELDS); th,_ = _first(r, THEME_FIELDS); m,_ = _first(r, MARKET_FIELDS); ld,_ = _first(r, LIST_DATE_FIELDS)
            tk = _norm_t(t)
            if tk: rows.append({"ticker":tk,"name":n,"sector":s,"industry":s,"sector_code":s,"theme":th,"market":m,"list_date":ld,"source_file":str(f),"source_field":_first(r,SECTOR_FIELDS)[1]})
    return {"normalizer_version":"V3510_MAPPING_NORMALIZER_V10","normalized_count":len(rows),"normalized_rows":rows,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}

def _load_json(p):
    obj = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(obj,list): return [x for x in obj if isinstance(x,dict)]
    if isinstance(obj,dict):
        for k in ("data","items","rows"):
            if isinstance(obj.get(k),list): return [x for x in obj[k] if isinstance(x,dict)]
    return []
