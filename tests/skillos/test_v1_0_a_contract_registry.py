"""Tests for SkillOS v1.0-A contract registry infrastructure."""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONTRACT_PATH = ROOT / "data/research_db/agent/registry/skill_contract_registry.json"
REGISTRY_PATH = ROOT / "data/research_db/agent/registry/skill_registry.generated.json"


@pytest.fixture
def contract_registry():
    assert CONTRACT_PATH.exists(), "contract registry not found"
    return json.loads(CONTRACT_PATH.read_text())


@pytest.fixture
def existing_registry():
    return json.loads(REGISTRY_PATH.read_text())


class TestContractRegistryExists:
    def test_contract_registry_exists(self, contract_registry):
        assert contract_registry is not None

    def test_contract_registry_valid_json(self, contract_registry):
        assert isinstance(contract_registry, dict)
        assert "contracts" in contract_registry


class TestContractCountMatches:
    def test_contract_count_matches_skill_registry(self, contract_registry, existing_registry):
        assert len(contract_registry["contracts"]) == len(existing_registry)

    def test_skill_ids_unique(self, contract_registry):
        ids = [c["skill_id"] for c in contract_registry["contracts"]]
        assert len(ids) == len(set(ids))

    def test_every_registered_skill_has_contract(self, contract_registry, existing_registry):
        registered = {s["skill_id"] for s in existing_registry}
        contracted = {c["skill_id"] for c in contract_registry["contracts"]}
        assert registered == contracted


class TestContractEntriesHaveSchemas:
    def test_contract_entries_have_input_schema(self, contract_registry):
        for c in contract_registry["contracts"]:
            assert c.get("input_schema"), f"{c['skill_id']}: missing input_schema"

    def test_contract_entries_have_output_schema(self, contract_registry):
        for c in contract_registry["contracts"]:
            assert c.get("output_schema"), f"{c['skill_id']}: missing output_schema"

    def test_output_schema_required_core_fields(self, contract_registry):
        cores = {"skill_id", "skill_version", "status", "risk_level", "input_hash", "output_hash"}
        for c in contract_registry["contracts"]:
            required = set(c["output_schema"].get("required", []))
            missing = cores - required
            assert not missing, f"{c['skill_id']}: output_schema missing {missing}"

    def test_risk_level_max_r2_draft(self, contract_registry):
        levels = {"R0_READ": 0, "R1_ANNOTATE": 1, "R2_DRAFT": 2}
        for c in contract_registry["contracts"]:
            rl = c.get("risk_level", "?")
            assert levels.get(rl, 99) <= 2, f"{c['skill_id']}: risk_level={rl} > R2_DRAFT"

    def test_no_forbidden_runtime_fields(self, contract_registry):
        forbidden = {"production", "broker", "real_trade", "broker_runtime",
                     "auto_buy", "auto_sell", "trade_allowed",
                     "buy", "sell", "order", "execution"}
        text = json.dumps(contract_registry).lower()
        found = [w for w in forbidden if w in text]
        assert not found, f"forbidden words in registry: {found}"


class TestLoaderReadOnly:
    def test_loader_read_only(self):
        from zmatrix.agent.skill_contract_registry import (
            load_skill_contract_registry,
            get_skill_contract,
            list_skill_contracts,
        )

        registry = load_skill_contract_registry()
        assert registry is not None
        assert "contracts" in registry
        assert len(registry["contracts"]) > 0

        contract = get_skill_contract("SYSTEM.GET_SKILLOS_STATUS")
        assert contract is not None
        assert contract["skill_id"] == "SYSTEM.GET_SKILLOS_STATUS"

        all_contracts = list_skill_contracts()
        assert len(all_contracts) == len(registry["contracts"])

        domain_contracts = list_skill_contracts(domain="GOVERNANCE")
        assert len(domain_contracts) > 0
        assert all(c["domain"] == "GOVERNANCE" for c in domain_contracts)

    def test_loader_returns_none_for_unknown(self):
        from zmatrix.agent.skill_contract_registry import get_skill_contract
        assert get_skill_contract("NONEXISTENT.SKILL") is None
