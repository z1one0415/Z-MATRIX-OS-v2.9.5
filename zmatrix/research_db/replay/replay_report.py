"""Batch-C: Replay Report — multi-section markdown report."""
from __future__ import annotations

class ReplayReport:
    @staticmethod
    def generate(result, manifest, audit, slices_count: int = 0) -> str:
        lines = ["# Replay Report", "", f"## Experiment", f"- ID: {result.experiment_id}",
                 f"- Status: {result.status}", f"- Slices: {result.slices_processed or slices_count}",
                 f"- Records: {result.total_records}", "",
                 "## Dataset", f"- Hash: {manifest.dataset_hash}",
                 f"- Factor: {manifest.factor_version}", f"- Parameters: {manifest.parameter_version}", "",
                 "## Audit", f"- Input Hash: {audit.input_hash}", f"- Output Hash: {audit.output_hash}",
                 f"- Replay Hash: {audit.replay_hash}",
                 f"- Reproducible: {audit.reproducible}", "",
                 "## Safety", "- Production: BLOCKED", "- Broker/runtime: BLOCKED"]
        return "\n".join(lines)
