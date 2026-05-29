"""V4.0-C1 DataForge — evidence data layer"""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class SourceRegistryItem:
    source_id: str; source_name: str; source_type: str; pit_safe: str
    usable_for_backtest: bool = False; usable_for_current_snapshot: bool = False
    usable_for_paper: bool = False; usable_for_production: bool = False
    license_status: str = "UNKNOWN"; refresh_frequency: str | None = None

@dataclass
class EvidenceCard:
    evidence_id: str; ticker: str | None = None; trade_date: str | None = None
    source_id: str = ""; field_name: str = ""; field_value: str | float | int | None = None
    as_of_date: str = ""; pit_status: str = "UNKNOWN"; freshness_status: str = "UNKNOWN"
    quality_score: float = 0.0; usable_for_production: bool = False
    evidence_hash: str = ""

class DataQualityScore:
    @staticmethod
    def compute(card: EvidenceCard) -> dict:
        score = 100
        if card.pit_status == "PIT_BLOCKED": score -= 40
        if card.freshness_status == "STALE": score -= 30
        if card.field_value is None: score -= 20
        status = "READY" if score >= 70 else "DATA_INSUFFICIENT" if score >= 40 else "STALE"
        return {"completeness": 100 if card.field_value else 0, "freshness": 100 if card.freshness_status=="FRESH" else 30, "pit_safety": 100 if card.pit_status=="PIT_SAFE" else 20, "final_score": max(0, score), "quality_status": status, "usable_for_production": False}

SOURCE_REGISTRY = [
    SourceRegistryItem("DS_R_PRICE","R Price OHLCV","market_data","YES",True,True,True),
    SourceRegistryItem("DS_B_FIN","B Financial Snapshot","fundamental","PARTIAL",False,True,True),
    SourceRegistryItem("DS_B_VAL","B Valuation","valuation","PARTIAL",False,True,False),
    SourceRegistryItem("DS_D_LIMIT","D Limit Structure","market_structure","PARTIAL",True,True,False),
]
