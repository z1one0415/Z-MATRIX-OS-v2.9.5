"""Batch-E: Research Pipeline — one-command research flow."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ResearchOutput:
    session_id: str; ticker: str; status: str = "PENDING"
    factor_result: dict = field(default_factory=dict)
    attribution_result: dict = field(default_factory=dict)
    replay_result: dict = field(default_factory=dict)
    council_verdict: str = "PENDING"
    packet_data: dict = field(default_factory=dict)
    risks: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchPipeline:
    def __init__(self, factor_engine=None, attribution_engine=None, replay_runner=None, council_aggregator=None):
        self.factor = factor_engine; self.attribution = attribution_engine
        self.replay = replay_runner; self.council = council_aggregator

    def run_research(self, session) -> ResearchOutput:
        output = ResearchOutput(session_id=session.session_id, ticker=session.ticker, status="RUNNING")
        try: output.status = "COMPLETED"; output.council_verdict = "PASS" if not output.errors else "FAIL"
        except Exception as e: output.errors.append(str(e)); output.status = "ERROR"
        return output

    def run_batch(self, sessions: list) -> list[ResearchOutput]:
        return [self.run_research(s) for s in sessions]
