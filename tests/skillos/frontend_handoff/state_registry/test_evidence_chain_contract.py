"""test_evidence_chain_contract.py — Evidence chain field verification tests.

Validates evidence chain node structure, hash presence, source class
distribution, no_real_source_flag enforcement, and gate linkage.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent  # Z-MATRIX-OS root

FIXTURE_PATH = ROOT / "tests" / "skillos" / "frontend_handoff" / "state_registry" / "gate_state_demo.json"

# Load from registry_loader for evidence chain
import sys
sys.path.insert(0, str(ROOT))
from skillos.frontend_handoff.state_registry.registry_loader import load_evidence_chain

chain = load_evidence_chain()
fixture = json.loads(FIXTURE_PATH.read_text())

VALID_SOURCE_CLASSES = {
    "COMMIT_LOG", "RESEARCH_ARTIFACT", "AUDIT_REPORT",
    "VALIDATION_OUTPUT", "FACTOR_RESULT", "HUMAN_REVIEW",
    "DECISION_GATE", "EXTERNAL_REFERENCE", "RUNTIME_LOG",
    "SCHEMA_DEFINITION"
}

VALID_VERIFICATION_STATUSES = {"UNVERIFIED", "VERIFIED", "STALE", "CORRUPT"}

SHA256_RE = re.compile(r'^[a-f0-9]{64}$')


def test_chain_has_required_top_fields():
    for field in ["chain_id", "generated_at", "nodes", "root_hash"]:
        assert field in chain, f"Evidence chain missing field: {field}"


def test_chain_id():
    assert chain["chain_id"] == "F7.2-evidence-chain"


def test_node_count_matches_gate_count():
    """Evidence nodes should equal gate count (11)."""
    assert len(chain["nodes"]) == len(fixture["gates"])
    assert len(chain["nodes"]) == 11


def test_all_nodes_have_required_fields():
    required = {"node_id", "hash", "hash_algorithm", "source_class",
                "no_real_source_flag", "linked_gate_id", "artifact_path",
                "commit_sha", "description", "verified_at", "verification_status"}
    for node in chain["nodes"]:
        for field in required:
            assert field in node, f"Node {node.get('node_id', 'UNKNOWN')} missing field: {field}"


def test_all_node_hashes_are_sha256():
    """All node hashes must be valid 64-char hex strings."""
    for node in chain["nodes"]:
        assert SHA256_RE.match(node["hash"]), \
            f"Node {node['node_id']} has invalid SHA-256 hash: {node['hash']}"
        assert node["hash_algorithm"] == "SHA-256", \
            f"Node {node['node_id']} has unexpected hash_algorithm: {node['hash_algorithm']}"


def test_all_node_source_classes_valid():
    for node in chain["nodes"]:
        assert node["source_class"] in VALID_SOURCE_CLASSES, \
            f"Node {node['node_id']} has invalid source_class: {node['source_class']}"


def test_no_real_source_flag_all_false():
    """All evidence nodes must have no_real_source_flag=false (real sources)."""
    for node in chain["nodes"]:
        assert node["no_real_source_flag"] is False, \
            f"Node {node['node_id']} has no_real_source_flag={node['no_real_source_flag']}"


def test_all_nodes_linked_to_valid_gate():
    """Every evidence node must link to a gate_id present in the fixture."""
    valid_gate_ids = {gate["gate_id"] for gate in fixture["gates"]}
    for node in chain["nodes"]:
        assert node["linked_gate_id"] in valid_gate_ids, \
            f"Node {node['node_id']} linked to unknown gate: {node['linked_gate_id']}"


def test_gate_ids_have_evidence_coverage():
    """Every gate must have at least one evidence node referencing it."""
    covered_gates = {node["linked_gate_id"] for node in chain["nodes"]}
    all_gates = {gate["gate_id"] for gate in fixture["gates"]}
    uncovered = all_gates - covered_gates
    assert not uncovered, f"Gates without evidence coverage: {uncovered}"


def test_all_verification_statuses_valid():
    for node in chain["nodes"]:
        assert node["verification_status"] in VALID_VERIFICATION_STATUSES, \
            f"Node {node['node_id']} invalid verification_status: {node['verification_status']}"


def test_all_nodes_verified():
    """All evidence nodes should have verification_status=VERIFIED."""
    for node in chain["nodes"]:
        assert node["verification_status"] == "VERIFIED", \
            f"Node {node['node_id']} not verified: {node['verification_status']}"


def test_root_hash_is_valid_sha256():
    assert SHA256_RE.match(chain["root_hash"]), \
        f"Invalid root_hash format: {chain['root_hash']}"


def test_root_hash_computed_correctly():
    """Root hash must equal SHA-256 of concatenated node hashes."""
    import hashlib
    combined = "".join(node["hash"] for node in chain["nodes"])
    expected = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    assert chain["root_hash"] == expected, \
        f"Root hash mismatch. Expected: {expected}, Got: {chain['root_hash']}"


def test_node_ids_unique():
    ids = [node["node_id"] for node in chain["nodes"]]
    assert len(ids) == len(set(ids)), f"Duplicate node_ids: {ids}"


def test_evidence_refs_consistent_with_nodes():
    """Gate evidence_refs must match node_ids in the evidence chain."""
    node_ids = {node["node_id"] for node in chain["nodes"]}
    for gate in fixture["gates"]:
        for ref in gate["evidence_refs"]:
            assert ref in node_ids, \
                f"Gate {gate['gate_id']} references unknown evidence node: {ref}"


def test_source_class_distribution():
    """Verify expected source class distribution."""
    classes = [node["source_class"] for node in chain["nodes"]]
    assert classes.count("RESEARCH_ARTIFACT") == 5  # F7.0, F7.2-plan, exec, exec-auth, safety
    assert classes.count("DECISION_GATE") == 2     # F7.2-final-auth, F7.2-decision
    assert classes.count("HUMAN_REVIEW") == 2       # F7.2-human-val-auth, F7.2-interpret
    assert classes.count("VALIDATION_OUTPUT") == 1  # F7.2-val-readonly
    assert classes.count("AUDIT_REPORT") == 1       # F7.2-val-audit
