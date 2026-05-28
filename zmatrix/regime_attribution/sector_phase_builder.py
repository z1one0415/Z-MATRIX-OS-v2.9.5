from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def build_sector_phase(*, sample: dict) -> dict:
    return {"phase":"UNKNOWN_SECTOR_PHASE","sector_data_status":"DATA_INSUFFICIENT","reason":"No sector price index data available; sector_map/ directory missing","uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
