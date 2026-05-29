"""V4.0-C3 Research Council — CouncilAggregator

Aggregates outputs from multiple independent reviewers into a single
research council decision. Only produces research-oriented statuses.
Never outputs BUY/SELL/AUTO_EXECUTE or any trading directives.
"""
from __future__ import annotations
from zmatrix.research_council.reviewers.base_reviewer import ReviewerResult

# Allowed output statuses only — no trade directives
ALLOWED_STATUSES = frozenset({
    "RESEARCH_SUPPORT",
    "RESEARCH_CONFLICT",
    "DATA_INSUFFICIENT",
    "RISK_REVIEW_REQUIRED",
})

FORBIDDEN_TERMS = frozenset({
    "BUY", "SELL", "STRONG_BUY", "STRONG_SELL", "AUTO_EXECUTE",
    "MARKET_ORDER", "LIMIT_ORDER", "STOP_LOSS_ORDER",
})


class CouncilAggregator:
    """Aggregates multiple reviewer outputs into a council decision."""

    @staticmethod
    def aggregate(results: list[ReviewerResult]) -> dict:
        """Aggregate reviewer results into a single council output.

        Returns:
            dict with:
            - council_status: one of ALLOWED_STATUSES
            - avg_score: average deterministic score
            - reviewer_count: number of reviewers
            - conflicts: list of conflicting reviewer pairs
            - risk_flags: union of all risk flags
            - real_trade_allowed: always False
            - broker_order_allowed: always False
            - production_allowed: always False
            - human_review_required: always True
            - paper_only: always True
        """
        if not results:
            return {
                "council_status": "DATA_INSUFFICIENT",
                "avg_score": 0.0,
                "reviewer_count": 0,
                "conflicts": [],
                "risk_flags": [],
                "real_trade_allowed": False,
                "broker_order_allowed": False,
                "production_allowed": False,
                "human_review_required": True,
                "paper_only": True,
            }

        # Collect scores and statuses
        scores = []
        risk_flags = set()
        insufficient = []
        supported = []

        for r in results:
            if r.review_status == "DATA_INSUFFICIENT":
                insufficient.append(r.reviewer_id)
            else:
                scores.append(r.deterministic_score)
                supported.append(r.reviewer_id)
            risk_flags.update(r.risk_flags)

        avg_score = sum(scores) / len(scores) if scores else 0.0

        # Determine council status
        if len(insufficient) > len(results) // 2:
            council_status = "DATA_INSUFFICIENT"
        elif avg_score < 30:
            council_status = "RISK_REVIEW_REQUIRED"
        elif max(scores) - min(scores) > 40 if len(scores) >= 2 else False:
            council_status = "RESEARCH_CONFLICT"
        else:
            council_status = "RESEARCH_SUPPORT"

        # Validate status is in allowed set
        if council_status not in ALLOWED_STATUSES:
            council_status = "RISK_REVIEW_REQUIRED"

        # Check for forbidden terms anywhere in results
        for r in results:
            for term in FORBIDDEN_TERMS:
                if term in str(r.facts) or term in str(r.score_trace) or term in str(r.risk_flags):
                    council_status = "RISK_REVIEW_REQUIRED"
                    risk_flags.add(f"FORBIDDEN_TERM_{term}")

        # Detect conflicts between reviewers
        conflicts = []
        if len(scores) >= 2:
            for i in range(len(scores)):
                for j in range(i + 1, len(scores)):
                    if abs(scores[i] - scores[j]) > 30:
                        conflicts.append({
                            "reviewer_a": supported[i],
                            "score_a": scores[i],
                            "reviewer_b": supported[j],
                            "score_b": scores[j],
                            "delta": abs(scores[i] - scores[j]),
                        })

        return {
            "council_status": council_status,
            "avg_score": round(avg_score, 2),
            "reviewer_count": len(results),
            "score_distribution": {
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 0,
                "count": len(scores),
            },
            "insufficient_reviewers": insufficient,
            "conflicts": conflicts,
            "risk_flags": sorted(risk_flags),
            "real_trade_allowed": False,
            "broker_order_allowed": False,
            "production_allowed": False,
            "human_review_required": True,
            "paper_only": True,
        }

    @staticmethod
    def validate_no_trade_terms(output: dict) -> bool:
        """Ensure no trading terms in council output."""
        output_str = str(output)
        for term in FORBIDDEN_TERMS:
            if term in output_str:
                return False
        return True
