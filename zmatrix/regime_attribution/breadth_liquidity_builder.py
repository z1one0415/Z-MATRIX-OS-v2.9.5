from __future__ import annotations
from zmatrix.regime_attribution.schema import DEFAULT_REGIME_ATTRIBUTION_SAFETY

def build_breadth_regime(*, sample: dict = None) -> dict:
    return {"breadth_status":"DATA_INSUFFICIENT","breadth_regime":"UNKNOWN","liquidity_regime":"UNKNOWN","volatility_regime":"UNKNOWN","reason":"Breadth computation requires scanning all tickers per entry_date; too expensive for 103K samples without precomputed index files","uses_future_data":False,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_ATTRIBUTION_SAFETY)}
