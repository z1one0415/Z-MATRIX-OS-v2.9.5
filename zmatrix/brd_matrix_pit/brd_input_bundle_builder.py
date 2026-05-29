# allowlist: forbidden-token-definition
"""BRD Input Bundle Builder — assemble B/R/D matrix for classify_stock_role"""
from __future__ import annotations
from zmatrix.brd_matrix_pit.b_matrix_pit_builder import build_b_matrix_pit
from zmatrix.brd_matrix_pit.r_matrix_pit_builder import build_r_matrix_pit
from zmatrix.brd_matrix_pit.d_matrix_pit_builder import build_d_matrix_pit
from zmatrix.brd_matrix_pit.account_exposure_stub import build_account_stub, build_exposure_stub
from zmatrix.brd_matrix_pit.schema import DEFAULT_BRD_MATRIX_PIT_SAFETY

def build_brd_input_bundle(*, ticker, replay_date, local_data_root, pit_features, event_snapshot=None, account=None, exposure=None):
    b = build_b_matrix_pit(ticker=ticker, replay_date=replay_date, local_data_root=local_data_root, pit_features=pit_features)
    r = build_r_matrix_pit(ticker=ticker, replay_date=replay_date, pit_features=pit_features)
    d = build_d_matrix_pit(ticker=ticker, replay_date=replay_date, pit_features=pit_features, event_snapshot=event_snapshot)
    acc = account if account is not None else build_account_stub()
    exp = exposure if exposure is not None else build_exposure_stub()
    ready = all(isinstance(x,dict) and x.get("status") in ("PASS","FAIL","WATCH","INSUFFICIENT_DATA") for x in (b,r,d))
    return {"bundle_version":"BRD_INPUT_BUNDLE_V10","ticker":ticker,"replay_date":replay_date,"input_ready":ready,
            "b_matrix":b,"r_matrix":r,"d_matrix":d,"account":acc,"exposure":exp,
            "safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY),"real_trade_allowed":False,"broker_order_allowed":False}
