"""Phase 4-F1: Candidate Factor Generator — Price/Volume/Momentum/Quality/Value/Sector/Event factors."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class FactorCategory(str, Enum):
    PRICE="PRICE"; VOLUME="VOLUME"; MOMENTUM="MOMENTUM"
    QUALITY="QUALITY"; VALUE="VALUE"; SECTOR="SECTOR"; EVENT="EVENT"

@dataclass
class FactorCandidate:
    factor_id: str; factor_name: str; category: FactorCategory
    formula_description: str = ""; universe: str = "ALL"
    parameters: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class CandidateFactorGenerator:
    @staticmethod
    def generate_price_factors() -> list[FactorCandidate]:
        return [FactorCandidate(f"PRICE_{i:03d}", f"Price_{i}", FactorCategory.PRICE, 
                f"Price-based factor {i}", parameters={"window": 5*i}) for i in range(1,4)]

    @staticmethod
    def generate_volume_factors() -> list[FactorCandidate]:
        return [FactorCandidate(f"VOL_{i:03d}", f"Volume_{i}", FactorCategory.VOLUME,
                parameters={"window": 5*i}) for i in range(1,4)]

    @staticmethod
    def generate_momentum_factors() -> list[FactorCandidate]:
        return [FactorCandidate(f"MOM_{i:03d}", f"Momentum_{i}", FactorCategory.MOMENTUM,
                parameters={"window": 20*i}) for i in range(1,4)]

    @staticmethod
    def generate_quality_factors() -> list[FactorCandidate]:
        return [FactorCandidate(f"QUAL_{i:03d}", f"Quality_{i}", FactorCategory.QUALITY,
                parameters={"metric": m}) for i, m in enumerate(["roe","gross_margin","debt_ratio"],1)]

    @staticmethod
    def generate_value_factors() -> list[FactorCandidate]:
        return [FactorCandidate(f"VAL_{i:03d}", f"Value_{i}", FactorCategory.VALUE,
                parameters={"metric": m}) for i, m in enumerate(["pe","pb","ps"],1)]

    @staticmethod
    def generate_all() -> list[FactorCandidate]:
        g = CandidateFactorGenerator
        return (g.generate_price_factors() + g.generate_volume_factors() +
                g.generate_momentum_factors() + g.generate_quality_factors() +
                g.generate_value_factors())
