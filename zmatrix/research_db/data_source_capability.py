"""ResearchDB Data Source Capability — registry and validation."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DataSourceCapability:
    data_source: str
    coverage: str = "UNKNOWN"
    historical_depth: str = "UNKNOWN"
    pit_safe: bool = False
    cost: str = "FREE"
    license: str = "PRIVATE"
    refresh_frequency: str = "MANUAL"
    usable_for_backtest: bool = False
    usable_for_current_snapshot: bool = False
    usable_for_production: bool = False


# Default registry
DEFAULT_SOURCE_REGISTRY: dict[str, DataSourceCapability] = {
    "manual_trade_import": DataSourceCapability(
        data_source="manual_trade_import",
        coverage="PERSONAL_ACCOUNT",
        historical_depth="UP_TO_5Y",
        pit_safe=False,
        usable_for_backtest=True,
        usable_for_current_snapshot=False,
        usable_for_production=False,
    ),
    "broker_export_file": DataSourceCapability(
        data_source="broker_export_file",
        coverage="PERSONAL_ACCOUNT",
        historical_depth="UP_TO_5Y",
        pit_safe=False,
        usable_for_backtest=True,
        usable_for_current_snapshot=False,
        usable_for_production=False,
    ),
    "daily_price_csv": DataSourceCapability(
        data_source="daily_price_csv",
        coverage="FULL_A_SHARE",
        historical_depth="UP_TO_5Y",
        pit_safe=True,
        usable_for_backtest=True,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
    "industry_mapping_manual": DataSourceCapability(
        data_source="industry_mapping_manual",
        coverage="MANUAL_CURATED",
        historical_depth="CURRENT",
        pit_safe=False,
        usable_for_backtest=False,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
    "financial_current_snapshot": DataSourceCapability(
        data_source="financial_current_snapshot",
        coverage="FULL_A_SHARE",
        historical_depth="CURRENT",
        pit_safe=False,
        usable_for_backtest=False,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
    "event_manual_input": DataSourceCapability(
        data_source="event_manual_input",
        coverage="MANUAL_CURATED",
        historical_depth="CURRENT",
        pit_safe=False,
        usable_for_backtest=False,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
    "caseforge_auto_event": DataSourceCapability(
        data_source="caseforge_auto_event",
        coverage="SYSTEM_GENERATED",
        historical_depth="CURRENT",
        pit_safe=False,
        usable_for_backtest=False,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
    "research_note_manual": DataSourceCapability(
        data_source="research_note_manual",
        coverage="MANUAL_CURATED",
        historical_depth="CURRENT",
        pit_safe=False,
        usable_for_backtest=False,
        usable_for_current_snapshot=True,
        usable_for_production=False,
    ),
}
