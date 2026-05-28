"""V4.0-0.6 Hardening: Pydantic schemas for governance layer"""
from __future__ import annotations
from typing import Literal, Optional

class HardgateStatus:
    def __init__(self, phase_id: str, baseline_version: str = "v3.5.20"):
        self.phase_id = phase_id; self.baseline_version = baseline_version
        self.real_trade_allowed = False; self.broker_order_allowed = False
        self.runtime_enabled = False; self.auto_buy_allowed = False
        self.auto_sell_allowed = False; self.production_strategy_modified = False
        self.classifier_production_modified = False
        self.max_promotion_status_allowed = "NO_PRODUCTION"
        self.baseline_rewritten = False

class DataSourceSchema:
    def __init__(self, ds_id, ds_name, coverage, pit_safe="UNKNOWN", cost="FREE", license_status="OWNED"):
        self.data_source_id = ds_id; self.data_source_name = ds_name; self.coverage = coverage
        self.pit_safe = pit_safe; self.cost_level = cost; self.license_status = license_status
        self.usable_for_backtest = pit_safe == "YES"; self.usable_for_current_snapshot = pit_safe in ("YES","PARTIAL")
        self.usable_for_paper = pit_safe in ("YES","PARTIAL"); self.usable_for_production = False
        self.missing_policy = "DATA_INSUFFICIENT"

class FactorRegistrySchema:
    def __init__(self, factor_id, factor_name, matrix_layer, data_source_id, pit_safe, trust_level):
        self.factor_id = factor_id; self.factor_name = factor_name; self.matrix_layer = matrix_layer
        self.data_source_id = data_source_id; self.pit_safe = pit_safe; self.trust_level = trust_level
        self.missing_policy = "DATA_INSUFFICIENT"; self.promotion_status = "BLOCKED_BY_PLATFORM_PHASE"
        self.net_return_ready = False; self.evidence_status_ready = False
        self.production_allowed = False; self.usable_for_backtest = False
        self.usable_for_current_snapshot = pit_safe in ("YES","PARTIAL"); self.usable_for_paper = pit_safe in ("YES","PARTIAL")

# H2: Schema validate
def validate_governance_schemas():
    h = HardgateStatus("v400-phase0"); assert h.real_trade_allowed is False
    ds = DataSourceSchema("test","Test","90%","YES"); assert ds.usable_for_backtest is True; assert ds.usable_for_production is False
    fr = FactorRegistrySchema("test","Test","B","ds","YES","T1"); assert fr.production_allowed is False; assert fr.promotion_status.startswith("BLOCKED")
    return True
