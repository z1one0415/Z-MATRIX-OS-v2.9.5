"""V4.0-1 Data Source Schema"""
from __future__ import annotations

class DataSourceCapability:
    def __init__(self, data_source_id, data_source_name, coverage, pit_safe="UNKNOWN", historical_depth=None, cost_level="FREE", license_status="OWNED", refresh_frequency=None):
        self.data_source_id = data_source_id; self.data_source_name = data_source_name; self.coverage = coverage; self.pit_safe = pit_safe; self.historical_depth = historical_depth; self.cost_level = cost_level; self.license_status = license_status; self.refresh_frequency = refresh_frequency
        self.usable_for_backtest = pit_safe == "YES"
        self.usable_for_current_snapshot = pit_safe in ("YES", "PARTIAL")
        self.usable_for_research = True
        self.usable_for_paper = pit_safe in ("YES", "PARTIAL")
        self.usable_for_production = False
        self.missing_policy = "DATA_INSUFFICIENT"
        self.fallback_policy = "NO_FALLBACK"

DATA_SOURCE_REGISTRY = {
    "r_price_ohlcv": {
        "data_source_id": "r_price_ohlcv", "data_source_name": "R Price OHLCV", "coverage": "99%+",
        "pit_safe": "YES", "historical_depth": "2021-2026", "cost_level": "FREE",
        "license_status": "OWNED", "refresh_frequency": "daily",
        "usable_for_backtest": True, "usable_for_current_snapshot": True,
        "usable_for_research": True, "usable_for_paper": True,
        "usable_for_production": False, "missing_policy": "DATA_INSUFFICIENT"
    },
    "b_financial_snapshot": {
        "data_source_id": "b_financial_snapshot", "data_source_name": "B Current Financial Snapshot",
        "coverage": "97%", "pit_safe": "PARTIAL", "historical_depth": "2026Q1 only",
        "cost_level": "FREE", "license_status": "OWNED",
        "usable_for_backtest": False, "usable_for_current_snapshot": True,
        "usable_for_research": True, "usable_for_paper": True,
        "usable_for_production": False, "missing_policy": "DATA_INSUFFICIENT"
    },
    "b_historical_pit_financial": {
        "data_source_id": "b_historical_pit_financial", "data_source_name": "B Historical PIT Financial",
        "coverage": "<10%", "pit_safe": "NO", "historical_depth": "2026Q1 only",
        "cost_level": "HIGH", "license_status": "UNKNOWN",
        "usable_for_backtest": False, "usable_for_current_snapshot": False,
        "usable_for_research": False, "usable_for_paper": False,
        "usable_for_production": False, "missing_policy": "BLOCK",
        "status": "BLOCKED_DATA_INSUFFICIENT"
    },
    "d_event_flow_theme": {
        "data_source_id": "d_event_flow_theme", "data_source_name": "D Event/Flow/Theme Data",
        "coverage": "<5%", "pit_safe": "UNKNOWN", "historical_depth": None,
        "cost_level": "HIGH", "license_status": "UNKNOWN",
        "usable_for_backtest": False, "usable_for_current_snapshot": False,
        "usable_for_research": False, "usable_for_paper": False,
        "usable_for_production": False, "missing_policy": "BLOCK",
        "status": "MISSING"
    },
    "trading_cost_model": {
        "data_source_id": "trading_cost_model", "data_source_name": "Trading Cost Model",
        "coverage": "paper-only", "pit_safe": "YES",
        "cost_level": "FREE", "license_status": "OWNED",
        "usable_for_backtest": True, "usable_for_current_snapshot": True,
        "usable_for_research": True, "usable_for_paper": True,
        "usable_for_production": False
    },
    "broker_runtime": {
        "data_source_id": "broker_runtime", "data_source_name": "Broker / Runtime Execution",
        "coverage": "N/A", "pit_safe": "NO",
        "cost_level": "UNKNOWN", "license_status": "NOT_ALLOWED",
        "usable_for_backtest": False, "usable_for_current_snapshot": False,
        "usable_for_research": False, "usable_for_paper": False,
        "usable_for_production": False, "missing_policy": "BLOCK",
        "status": "BLOCKED"
    }
}

PIT_POLICIES = {
    "PIT_SAFE": {"usable_for_backtest": True, "promotion_allowed": "RESEARCH_READY"},
    "PIT_PARTIAL": {"usable_for_backtest": False, "promotion_allowed": "RESEARCH_ONLY"},
    "PIT_BLOCKED": {"usable_for_backtest": False, "promotion_allowed": "BLOCKED_BY_PIT"},
    "PIT_UNKNOWN": {"usable_for_backtest": False, "promotion_allowed": "BLOCKED_BY_PIT"}
}

TTL_POLICIES = {
    "FRESH": {"ttl_days": None, "action": "USE"},
    "ACCEPTABLE": {"ttl_days": None, "action": "USE_WITH_WARNING"},
    "STALE": {"ttl_days": None, "action": "DATA_INSUFFICIENT"},
    "MISSING": {"ttl_days": None, "action": "DATA_INSUFFICIENT"},
    "CONFLICTED": {"ttl_days": None, "action": "DATA_INSUFFICIENT"}
}

MISSING_POLICIES = {
    "BLOCK": "Do not use the data source; halt the pipeline",
    "DATA_INSUFFICIENT": "Mark as insufficient; do not generate signals",
    "ALLOW_PROXY": "Use proxy; must be marked as proxy",
    "IGNORE": "Skip the missing data; do not block the pipeline"
}

class DataUsagePermission:
    RESEARCH_ONLY = "RESEARCH_ONLY"
    CURRENT_SNAPSHOT_ONLY = "CURRENT_SNAPSHOT_ONLY"
    BACKTEST_ALLOWED = "BACKTEST_ALLOWED"
    PAPER_ALLOWED = "PAPER_ALLOWED"
    PRODUCTION_BLOCKED = "PRODUCTION_BLOCKED"
    DATA_INSUFFICIENT = "DATA_INSUFFICIENT"
