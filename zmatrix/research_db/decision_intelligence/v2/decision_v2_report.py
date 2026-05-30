"""V2 Report — Markdown + JSON summary of Prediction Market, Calibration, and Rankings."""
from __future__ import annotations
import json

class DecisionReportV2:
    @staticmethod
    def generate_markdown(market: dict, calibrations: list, rankings: list) -> str:
        lines = ["# Decision Intelligence V2 Report", "", "## Prediction Market", f"- Ticker: {market.get('ticker','N/A')}",
                 f"- Consensus: {market.get('consensus_direction','FLAT')} ({market.get('consensus_magnitude',0):.0f}bps)",
                 f"- Forecaster count: {market.get('forecaster_count',0)}", f"- Agreement: {market.get('agreement_ratio',0):.0%}",
                 "", "## Calibration", "| Forecaster | Accuracy | Confidence | Overconf | Grade |",
                 "|------------|:--:|:--:|:--:|:--:|"]
        for c in calibrations:
            lines.append(f"| {c.forecaster_id} | {c.actual_accuracy:.0%} | {c.mean_confidence:.0%} | {c.overconfidence_score:+.2f} | {c.calibration_grade} |")
        lines.extend(["", "## Researcher Rankings", "| Rank | Forecaster | Score | Trend |", "|:--:|------------|:--:|:--:|"])
        for r in rankings[:10]:
            lines.append(f"| {r.rank} | {r.forecaster_id} | {r.composite_score:.3f} | {r.trend} |")
        lines.extend(["", "## Safety", "- Production: BLOCKED", "- Broker/runtime: BLOCKED"])
        return "\n".join(lines)

    @staticmethod
    def generate_json(market: dict, rankings: list) -> str:
        return json.dumps({"market": market, "rankings": [{"id":r.forecaster_id,"rank":r.rank,"score":r.composite_score,"trend":r.trend} for r in rankings],
                          "production_allowed": False, "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}, indent=2)
