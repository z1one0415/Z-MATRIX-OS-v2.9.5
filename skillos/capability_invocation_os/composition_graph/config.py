"""Composition Graph configuration — P0 disabled by default."""

_GRAPH_ENABLED = False


def is_composition_graph_enabled() -> bool:
    return _GRAPH_ENABLED


def set_composition_graph_enabled(value: bool) -> None:
    global _GRAPH_ENABLED
    _GRAPH_ENABLED = value
