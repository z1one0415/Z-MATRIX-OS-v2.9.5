"""EV2: Hypothesis Mutator — variant generation from failed hypotheses."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class MutationResult:
    mutation_id: str; parent_hypothesis: str; mutation_type: str; description: str
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class HypothesisMutator:
    MUTATION_TYPES = {"INVERT_SIGN": "Reverse factor direction", "EXTEND_HORIZON": "Increase holding period",
        "ADD_CONSTRAINT": "Add quality filter", "REMOVE_CONSTRAINT": "Remove existing filter",
        "COMBINE": "Combine with another factor", "SPLIT": "Split into sub-factors"}

    @staticmethod
    def generate_variants(hypothesis_id: str, reason: str = "LOW_IC") -> list[MutationResult]:
        return [MutationResult(mutation_id=f"{hypothesis_id}-{mt}", parent_hypothesis=hypothesis_id, mutation_type=mt, description=desc)
                for mt, desc in HypothesisMutator.MUTATION_TYPES.items()]
