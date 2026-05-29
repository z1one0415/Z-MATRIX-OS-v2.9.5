"""V4.0-Hardening-C3 IRF module — 8 chain integration functions"""
from __future__ import annotations

from zmatrix.irf.irf_chain import (
    irf01_full_chain,
    irf02_monthly_selection_chain,
    irf03_factor_chain,
    irf04_execution_chain,
    irf05_account_review_chain,
    irf06_portfolio_alpha_chain,
    irf07_multi_strategy_chain,
    irf08_factor_data_chain,
)

__all__ = [
    "irf01_full_chain",
    "irf02_monthly_selection_chain",
    "irf03_factor_chain",
    "irf04_execution_chain",
    "irf05_account_review_chain",
    "irf06_portfolio_alpha_chain",
    "irf07_multi_strategy_chain",
    "irf08_factor_data_chain",
]
