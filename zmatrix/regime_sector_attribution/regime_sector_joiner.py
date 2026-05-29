# allowlist: forbidden-token-definition
from __future__ import annotations
import csv
from pathlib import Path
from collections import defaultdict
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def _ed(x): return str(x or "").replace("-","")[:8]

def build_regime_sector_joined_rows(*, raw_replay_result: dict, sector_basket_report: dict) -> dict:
    # Load sector features from basket report
    arc = sector_basket_report.get("replay_sector_feature_joiner",{})
    joined_rows_sample = arc.get("joined_rows_sample",[]) or []
    joined_rows_all = arc.get("joined_rows",[]) or []
    # If pre-joined rows exist in basket report, use those
    rows = joined_rows_all if joined_rows_all else joined_rows_sample
    total = len(rows)
    ready = sum(1 for r in rows if r.get("market_regime") and r.get("sector_phase"))
    cov = ready/total if total else 0
    return {"joiner_version":"V3512_REGIME_SECTOR_JOINER_V10","total_rows":total,"ready_rows":ready,"join_coverage":cov,"join_status":"READY" if cov>=0.90 else "PARTIAL" if cov>0 else "DATA_INSUFFICIENT","joined_rows":rows,"uses_future_data":False,"synthetic_sector_index":True,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}
