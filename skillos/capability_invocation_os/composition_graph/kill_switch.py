"""Composition Graph kill switches — all active (killed) for P0."""


def should_force_disabled() -> bool:
    return True


def should_block_execution() -> bool:
    return True


def should_block_mutable_state() -> bool:
    return True


def should_block_real_source() -> bool:
    return True
