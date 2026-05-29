# allowlist: forbidden-token-definition
"""Account/Exposure Stubs — safe empty shells, no real account"""
from __future__ import annotations
from zmatrix.brd_matrix_pit.schema import DEFAULT_BRD_MATRIX_PIT_SAFETY
def build_account_stub():
    return {"account_version":"ACCOUNT_STUB_V10","violation_reasons":[],"real_account_connected":False,
            "real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY)}
def build_exposure_stub():
    return {"exposure_version":"EXPOSURE_STUB_V10","warnings":[],"portfolio_connected":False,
            "real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_BRD_MATRIX_PIT_SAFETY)}
