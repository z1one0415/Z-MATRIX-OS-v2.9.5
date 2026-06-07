"""
Level 4 warning evaluation pipeline.

P0: disabled path only. Enabled path returns a disabled placeholder.
No warning emission. No file I/O. No stdout/stderr. No blocking.
"""

from skillos.level4.config import Level4Config, load_config
from skillos.level4.guards import is_level4_enabled, disabled_guard
from skillos.level4.models import Level4EvaluationInput, Level4EvaluationResult


def evaluate_level4(
    evaluation_input: Level4EvaluationInput,
    config: Level4Config,
) -> Level4EvaluationResult:
    """
    Evaluate Level 4 warning conditions.

    If Level 4 is disabled (default), immediately return CONTINUE
    with no warnings and no side effects.

    If Level 4 is enabled (P0 placeholder), return a disabled-style
    placeholder. The enabled path is NOT IMPLEMENTED in P0 and must
    not emit any warnings.
    """
    if not is_level4_enabled(config):
        return disabled_guard(config)

    # P0: enabled path is a placeholder only.
    # No warning emission. No side effects. No file I/O.
    return disabled_guard(config)
