"""Batch-D: Devil Advocate — mandatory counter-evidence."""
from __future__ import annotations

class DevilReviewer:
    @staticmethod
    def challenge(ctx: dict) -> dict:
        challenges = []
        if ctx.get("metrics",{}).get("coverage",1) < 0.5: challenges.append("Low coverage → survivorship bias")
        if abs(ctx.get("metrics",{}).get("ic",0)) < 0.02: challenges.append("IC near zero → possible noise")
        if ctx.get("risk_flags"): challenges.append(f"Risk flags: {ctx['risk_flags']}")
        if not ctx.get("replay_hash"): challenges.append("Missing replay hash → not reproducible")
        return {"challenges": challenges, "challenge_count": len(challenges), "requires_attention": len(challenges) > 0, "production_allowed": False}

    @staticmethod
    def mandatory_review(ctx: dict) -> str:
        """Every council result MUST include devil's advocate opinion."""
        c = DevilReviewer.challenge(ctx)
        return f"Devil challenges: {len(c['challenges'])} issues. {'⚠️ REQUIRES ATTENTION' if c['requires_attention'] else '✅ No critical challenges'}"
