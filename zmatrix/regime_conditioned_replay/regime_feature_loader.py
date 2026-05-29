# allowlist: forbidden-token-definition
from __future__ import annotations
from zmatrix.regime_attribution.market_index_loader import load_index_data
from zmatrix.regime_attribution.market_regime_builder import build_market_regime
from zmatrix.regime_conditioned_replay.schema import DEFAULT_REGIME_REPLAY_SAFETY

def load_regime_features(*, joined: list[dict], data_root: str = ".", max_items: int | None = None) -> dict:
    idx_data = load_index_data(data_root=data_root)
    idx = idx_data.get("index_data",{}).get("000001", idx_data.get("index_data",{}).get(list(idx_data.get("index_data",{}).keys())[0], {})) if idx_data.get("index_data") else {}
    items = joined[:max_items] if max_items else joined
    rows = []
    for s in items:
        mr = build_market_regime(sample=s, index_data=idx)
        rows.append({**s,"market_regime":mr.get("regime","UNKNOWN_MARKET_REGIME"),"liquidity_regime":"LIQUIDITY_CONTRACTION" if "LIQUIDITY_CONTRACTION" in mr.get("all_regimes",[]) else "LIQUIDITY_EXPANSION" if "LIQUIDITY_EXPANSION" in mr.get("all_regimes",[]) else "NORMAL","regime_feature_status":"READY" if mr.get("regime_data_status")=="READY" else "DATA_INSUFFICIENT","uses_future_data":False})
    return {"feature_status":"READY","rows":rows,"indexes_available":idx_data.get("available_indexes",[]),"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_REPLAY_SAFETY)}
