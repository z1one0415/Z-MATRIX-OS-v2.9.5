from __future__ import annotations
import math
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY, DECAY_HALF_LIFE

def calculate_data_decay_penalty(*, matrix_type: str, age_days: int | None, ttl_days: int | None) -> dict:
    mt = matrix_type.upper()
    if age_days is None or ttl_days is None: penalty=0.80; status="DECAY_DATA_INSUFFICIENT"
    elif age_days <= ttl_days: penalty=0.0; status="NO_DECAY"
    else: half = DECAY_HALF_LIFE.get(mt,ttl_days); penalty=min(0.80,1-math.exp(-(age_days-ttl_days)/max(1,half))); status="DECAY_REQUIRED"
    return {"decay_version":"V359_DATA_DECAY_PENALTY_PREVIEW_V10","matrix_type":mt,"age_days":age_days,"ttl_days":ttl_days,"decay_penalty":penalty,"decay_status":status,"production_weight_adjustment_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
