"""F2-B: Rolling Window Engine — fixed-size sliding windows."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class RollingWindowResult:
    window_id: str; start_idx: int; end_idx: int; ic: float = 0.0
    rankic: float = 0.0; hit_rate: float = 0.0; sample_size: int = 0
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class RollingWindowEngine:
    @staticmethod
    def generate_windows(data: list[dict], window_size: int = 60, step: int = 20) -> list[dict]:
        windows = []
        for i in range(0, len(data) - window_size + 1, step):
            windows.append({"start": i, "end": i + window_size, "data": data[i:i+window_size]})
        return windows

    @staticmethod
    def compute_ic_series(windows: list[dict]) -> list[float]:
        ics = []
        for w in windows:
            ic_vals = [d.get("ic",0) for d in w["data"] if d.get("ic") is not None]
            ics.append(sum(ic_vals)/len(ic_vals) if ic_vals else 0.0)
        return ics
