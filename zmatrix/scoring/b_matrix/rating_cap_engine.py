from __future__ import annotations
from .contracts import BRating, TrapFlag, TrapSeverity

_ORDER = {BRating.A: 4, BRating.B: 3, BRating.C: 2, BRating.D: 1}


def lower_cap(current: BRating, new_cap: BRating) -> BRating:
    return new_cap if _ORDER[new_cap] < _ORDER[current] else current


def cap_from_traps(traps: list[TrapFlag]) -> BRating:
    cap = BRating.A
    for t in traps:
        if t.severity == TrapSeverity.REJECT:
            cap = lower_cap(cap, BRating.D)
        elif t.severity == TrapSeverity.CAP_C:
            cap = lower_cap(cap, BRating.C)
        elif t.severity == TrapSeverity.CAP_B:
            cap = lower_cap(cap, BRating.B)
    return cap


def apply_rating_cap(rating: BRating, cap: BRating) -> BRating:
    return cap if _ORDER[cap] < _ORDER[rating] else rating


def rating_from_score(score: float) -> BRating:
    if score >= 8.0:
        return BRating.A
    if score >= 6.5:
        return BRating.B
    if score >= 5.0:
        return BRating.C
    return BRating.D


def eligibility_from_rating(rating: BRating, has_traps: bool):
    from .contracts import BEligibility
    if rating == BRating.A:
        return BEligibility.B_ELIGIBLE if not has_traps else BEligibility.B_WATCH
    if rating == BRating.B:
        return BEligibility.B_WATCH
    if rating == BRating.C:
        return BEligibility.B_REVIEW
    return BEligibility.B_DISQUALIFIED
