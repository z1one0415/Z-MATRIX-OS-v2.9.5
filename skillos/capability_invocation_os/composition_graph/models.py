"""Composition Graph data models."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CompositionGraphDecision(Enum):
    ALLOW_GRAPH_READONLY_SUMMARY = "ALLOW_GRAPH_READONLY_SUMMARY"
    DENY_GRAPH_SOURCE_FORBIDDEN = "DENY_GRAPH_SOURCE_FORBIDDEN"
    DENY_GRAPH_REAL_SOURCE_FORBIDDEN = "DENY_GRAPH_REAL_SOURCE_FORBIDDEN"
    DENY_GRAPH_OUTPUTS_UNSAFE = "DENY_GRAPH_OUTPUTS_UNSAFE"
    DENY_GRAPH_BRIDGE_DENIED = "DENY_GRAPH_BRIDGE_DENIED"
    DENY_GRAPH_EXECUTION_FORBIDDEN = "DENY_GRAPH_EXECUTION_FORBIDDEN"
    DENY_GRAPH_FACTOR_DENIED = "DENY_GRAPH_FACTOR_DENIED"
    DISABLED_DEFAULT_NOOP = "DISABLED_DEFAULT_NOOP"


@dataclass(frozen=True)
class CompositionGraphNode:
    node_id: str = ""
    node_type: str = "graph_noop"
    payload: Any = field(default_factory=dict)
    hash_value: str = ""


@dataclass(frozen=True)
class CompositionGraphEdge:
    edge_id: str = ""
    edge_type: str = "graph_to_noop"
    source_node_id: str = ""
    target_node_id: str = ""
    hash_value: str = ""


@dataclass(frozen=True)
class CompositionGraphEvidence:
    source_commit: str = ""
    source_class: str = "factor_library_fixture"
    no_real_source_flag: bool = True
    fixture_source_commit: str = "P1_FIXTURE_ONLY"
    graph_node_hash: str = ""
    graph_edge_hash: str = ""
    a1_evidence_hash: str = ""
    permission_tier: str = "T0"
    forbidden_outputs_removed_hash: str = ""
    rollback_marker: bool = False
    privacy_marker: bool = True
    c1_handoff_marker: bool = True


@dataclass(frozen=True)
class DeniedGraphContext:
    node_id: str = ""
    original_decision: str = ""
    reason: str = ""


@dataclass(frozen=True)
class GraphSourceSummary:
    source_class: str = ""
    total_nodes: int = 0
    total_edges: int = 0
    allowed: int = 0
    denied: int = 0


@dataclass(frozen=True)
class CompositionGraphResponse:
    response_id: str = ""
    decision: CompositionGraphDecision = field(
        default_factory=lambda: CompositionGraphDecision.DISABLED_DEFAULT_NOOP
    )
    nodes: list = field(default_factory=list)
    edges: list = field(default_factory=list)
    evidence: Any = field(default_factory=dict)
    forbidden_outputs_removed: list = field(default_factory=list)
    degraded: bool = True
    mode: str = "DISABLED_DEFAULT_P0"
    graph_enabled: bool = False
    execution_enabled: bool = False
