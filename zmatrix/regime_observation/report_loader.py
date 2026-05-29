# allowlist: forbidden-token-definition
from __future__ import annotations
import json
from pathlib import Path
from zmatrix.regime_observation.schema import DEFAULT_REGIME_OBSERVATION_SAFETY

def _lj(p):
    x = Path(p)
    return json.loads(x.read_text(encoding="utf-8")) if x.exists() else None

def load_v357_closeout_reports(*, replay_path: str, anti_overfit_path: str, governance_path: str) -> dict:
    replay = _lj(replay_path); anti = _lj(anti_overfit_path); gov = _lj(governance_path)
    missing = []
    if replay is None: missing.append(replay_path)
    if anti is None: missing.append(anti_overfit_path)
    if gov is None: missing.append(governance_path)
    return {"loader_version":"V358_REPORT_LOADER_V10","load_status":"READY" if not missing else "OBSERVATION_BLOCKED_MISSING_INPUT_REPORTS","missing_reports":missing,"replay_report":replay or {},"anti_overfit_report":anti or {},"governance_report":gov or {},"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_REGIME_OBSERVATION_SAFETY)}
