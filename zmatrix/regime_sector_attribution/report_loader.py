from __future__ import annotations
import json
from pathlib import Path
from zmatrix.regime_sector_attribution.schema import DEFAULT_REGIME_SECTOR_SAFETY

def load_joint_attribution_inputs(*, regime_replay_report_path: str, sector_basket_report_path: str, raw_replay_path: str) -> dict:
    rp = _l(regime_replay_report_path); sp = _l(sector_basket_report_path); rw = _l(raw_replay_path)
    missing = []
    if rp is None: missing.append(regime_replay_report_path)
    if sp is None: missing.append(sector_basket_report_path)
    if rw is None: missing.append(raw_replay_path)
    return {"loader_version":"V3512_REPORT_LOADER_V10","load_status":"READY" if not missing else "DATA_INSUFFICIENT","missing_reports":missing,"regime_replay_report":rp or {},"sector_basket_report":sp or {},"raw_replay_result":rw or {},"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_SECTOR_SAFETY)}

def _l(p):
    x = Path(p)
    return json.loads(x.read_text(encoding="utf-8")) if x.exists() else None
