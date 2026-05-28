from __future__ import annotations
from collections import defaultdict
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

def build_synthetic_sector_basket_preview(*, sector_mapping: dict, max_sectors: int | None = None) -> dict:
    grouped = defaultdict(list)
    for ticker, meta in (sector_mapping or {}).items():
        sec = meta.get("sector")
        if sec: grouped[sec].append(ticker)
    sectors = dict(grouped)
    if max_sectors: sectors = dict(list(sectors.items())[:max_sectors])
    return {"basket_version":"V359_SYNTHETIC_SECTOR_BASKET_PREVIEW_V10","synthetic_sector_index":True,"synthetic_index_warning":True,"production_index_allowed":False,"sector_count":len(sectors),"sector_members":sectors,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
