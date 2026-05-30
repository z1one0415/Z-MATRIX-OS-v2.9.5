"""Batch-C: Replay Manifest — immutable experiment evidence."""
from __future__ import annotations
import json
from dataclasses import dataclass, field

@dataclass
class ReplayManifest:
    experiment_id: str; dataset_hash: str; factor_version: str
    parameter_version: str; replay_hash: str; created_at: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

    def to_json(self) -> str:
        return json.dumps({"experiment_id":self.experiment_id,"dataset_hash":self.dataset_hash,
                          "factor_version":self.factor_version,"parameter_version":self.parameter_version,
                          "replay_hash":self.replay_hash,"created_at":self.created_at}, indent=2)

    @staticmethod
    def from_experiment(record, replay_hash: str) -> "ReplayManifest":
        return ReplayManifest(experiment_id=record.experiment_id, dataset_hash=record.dataset_hash,
                              factor_version=record.factor_version, parameter_version=record.parameter_version,
                              replay_hash=replay_hash, created_at=record.created_time if hasattr(record,'created_time') else "")
