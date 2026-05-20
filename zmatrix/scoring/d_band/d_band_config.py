from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


@dataclass(frozen=True, slots=True)
class DBandConfig:
    weights: dict[str, float] = field(default_factory=lambda: {
        "blackhorse_gene": 0.40,
        "sector_ignition": 0.30,
        "vol_price_preload": 0.20,
        "theme_mapping": 0.10,
    })
    thresholds: dict[str, float] = field(default_factory=lambda: {
        "watch_score": 6.0,
        "d3_candidate_score": 7.2,
        "sector_ignition": 0.65,
        "blackhorse_gene_preheat": 6.2,
        "blackhorse_gene_d3": 7.0,
        "vol_price_preload_d3": 6.0,
    })
    caps: dict[str, Any] = field(default_factory=lambda: {
        "missing_theme_seed_score_ceiling": 7.6,
        "phase1_lifecycle_max": "D3_CANDIDATE",
        "phase1_execution_mode": "paper",
        "phase1_real_trade_allowed": False,
    })


def load_config(path: str | Path | None = None) -> DBandConfig:
    if path is None or yaml is None:
        return DBandConfig()
    p = Path(path)
    if not p.exists():
        return DBandConfig()
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    default = DBandConfig()
    return DBandConfig(
        weights={**default.weights, **raw.get("weights", {})},
        thresholds={**default.thresholds, **raw.get("thresholds", {})},
        caps={**default.caps, **raw.get("caps", {})},
    )
