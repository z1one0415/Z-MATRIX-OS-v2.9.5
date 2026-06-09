"""Composition Graph registry — static P0 placeholder."""

from skillos.capability_invocation_os.composition_graph.constants import GRAPH_MODE

_REGISTRY: dict[str, dict] = {}


def get_graph_mode() -> str:
    """Return the current graph mode."""
    return GRAPH_MODE


def is_registered(graph_id: str) -> bool:
    """Check if a graph ID is registered."""
    return graph_id in _REGISTRY


def register_graph(graph_id: str, metadata: dict | None = None) -> None:
    """Register a graph (P0: no-op placeholder)."""
    _REGISTRY[graph_id] = metadata or {}


def unregister_graph(graph_id: str) -> None:
    """Unregister a graph (P0: no-op placeholder)."""
    _REGISTRY.pop(graph_id, None)


def list_registered() -> list[str]:
    """List all registered graph IDs."""
    return list(_REGISTRY.keys())


def clear_registry() -> None:
    """Clear all registered graphs."""
    _REGISTRY.clear()
