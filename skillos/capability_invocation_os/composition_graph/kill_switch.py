"""Composition Graph kill switch — P0 always force-disabled."""

_FORCE_DISABLED = True


def should_force_disabled() -> bool:
    return _FORCE_DISABLED


def set_force_disabled(value: bool) -> None:
    global _FORCE_DISABLED
    _FORCE_DISABLED = value
