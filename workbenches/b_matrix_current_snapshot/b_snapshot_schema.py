"""V4.0-4 B-Matrix Current Snapshot Workbench"""
from __future__ import annotations

B_SNAPSHOT_FIELDS = ["ticker","name","sector","b_score","tier","roe","gross_margin","netprofit_yoy","revenue_yoy","debt_ratio","ocfps","pe_ttm","pb","industry_roe_pct","hard_gate_passed","reason_codes","missing_fields","valuation_source","cashflow_source"]
B_TIERS = ["B_CORE_STRONG","B_CORE_WATCH","B_CORE_DATA_GAP","B_CORE_VALUATION_RISK","B_CORE_CASHFLOW_PROXY"]
B_SNAPSHOT_PERMISSIONS = {"mode":"CURRENT_SNAPSHOT_ONLY","historical_pit":"BLOCKED_DATA_INSUFFICIENT","production":"BLOCKED","backtest":"BLOCKED","paper":"ALLOWED","research":"ALLOWED"}

class BSnapshotItem:
    def __init__(self, ticker, name=None, sector=None, b_score=0, tier="B_CORE_WATCH"):
        self.ticker = ticker; self.name = name; self.sector = sector; self.b_score = b_score; self.tier = tier; self.roe = None; self.gross_margin = None; self.netprofit_yoy = None; self.revenue_yoy = None; self.debt_ratio = None; self.ocfps = None; self.pe_ttm = None; self.pb = None; self.industry_roe_pct = None; self.hard_gate_passed = False; self.reason_codes = []; self.missing_fields = []; self.valuation_source = "eps_bps_estimate"; self.cashflow_source = "ocfps_proxy"; self.real_trade_allowed = False; self.broker_order_allowed = False; self.production_allowed = False
