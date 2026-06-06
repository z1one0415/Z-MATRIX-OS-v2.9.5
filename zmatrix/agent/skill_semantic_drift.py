"""Semantic drift detection for SkillOS v1.1-B.

Compares current state against frozen baseline snapshot.
Audit-only: never blocks, never writes files, never calls invoke_skill.
"""

import json
import hashlib
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent.parent
BASELINE_PATH = ROOT / "data" / "research_db" / "agent" / "baselines" / "skillos_v1_1_b_semantic_drift_baseline.json"

REQUIRED_TARGETS = ["contract_registry", "hash_policy", "golden_hash_lock", "golden_regression"]

_cache: Optional[dict] = None
_current_cache: Optional[dict] = None


def canonical_json_hash(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_baseline_snapshot() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(BASELINE_PATH.read_text())
    return _cache


def build_current_snapshot() -> dict:
    global _current_cache
    if _current_cache is not None:
        return _current_cache

    cr_path = ROOT / "data" / "research_db" / "agent" / "registry" / "skill_contract_registry.json"
    cr = json.loads(cr_path.read_text())
    contracts = cr["contracts"]
    schema_proj = [
        {
            "skill_id": c["skill_id"],
            "input_schema": c.get("input_schema", {}),
            "output_schema": c.get("output_schema", {}),
            "risk_level": c.get("risk_level"),
            "semantic_category": c.get("semantic_category"),
            "status": c.get("status"),
        }
        for c in contracts
    ]

    hp_path = ROOT / "zmatrix/agent/skill_hash_policy.py"
    golden_path = ROOT / "data/research_db/agent/golden/skillos_v1_0_d_golden_cases.json"
    golden = json.loads(golden_path.read_text())
    reg_path = ROOT / "data/research_db/agent/golden/skillos_v1_0_f_golden_regression_cases.json"
    reg = json.loads(reg_path.read_text())

    _current_cache = {
        "contract_registry": {
            "path": str(cr_path.relative_to(ROOT)),
            "contract_count": len(contracts),
            "unique_skill_id_count": len({c["skill_id"] for c in contracts}),
            "sha256": file_sha256(cr_path),
            "schema_projection_sha256": canonical_json_hash(schema_proj),
        },
        "hash_policy": {
            "path": "zmatrix/agent/skill_hash_policy.py",
            "hash_algorithm": _extract_hash_algorithm(hp_path),
            "excluded_output_fields": _extract_excluded_fields(hp_path),
            "sha256": file_sha256(hp_path),
        },
        "golden_hash_lock": {
            "path": "data/research_db/agent/golden/skillos_v1_0_d_golden_cases.json",
            "case_count": len(golden.get("cases", [])),
            "sha256": file_sha256(golden_path),
        },
        "golden_regression": {
            "path": "data/research_db/agent/golden/skillos_v1_0_f_golden_regression_cases.json",
            "case_count": len(reg.get("cases", [])),
            "domains_covered": len({c["domain"] for c in reg.get("cases", [])}),
            "sha256": file_sha256(reg_path),
        },
    }
    return _current_cache


def _extract_hash_algorithm(path: Path) -> str:
    text = path.read_text()
    for line in text.split("\n"):
        if "HASH_ALGORITHM" in line and "=" in line and '"' in line:
            return line.split('"')[1]
    return "UNKNOWN"


def _extract_excluded_fields(path: Path) -> list:
    text = path.read_text()
    for line in text.split("\n"):
        if "OUTPUT_HASH_EXCLUDED_FIELDS" in line and "=" in line:
            start = line.index("[")
            end = line.index("]") + 1
            return eval(line[start:end])
    return []


def compare_snapshots(baseline: dict, current: dict) -> dict:
    targets = []
    max_sev = "INFO"
    drift = False

    for name in REQUIRED_TARGETS:
        b = baseline["targets"].get(name, {})
        c = current.get(name, {})
        sev = _compare_target(name, b, c)
        targets.append({"target": name, "severity": sev})
        if sev in ("FAIL_CI",):
            drift = True
            if max_sev != "FAIL_CI":
                max_sev = "FAIL_CI"
        elif sev == "WARN" and max_sev == "INFO":
            max_sev = "WARN"

    summary = {t["target"]: t["severity"] for t in targets}
    return {
        "mode": "STANDALONE_SEMANTIC_DRIFT_AUDIT",
        "drift_detected": drift,
        "max_severity": max_sev,
        "targets": targets,
        "summary": summary,
        "runtime_action": "NONE",
        "blocked": False,
        "enforcement": "DISABLED",
    }


def _compare_target(name: str, baseline_t: dict, current_t: dict) -> str:
    if name == "contract_registry":
        if baseline_t.get("contract_count", 0) != current_t.get("contract_count", 0):
            return "FAIL_CI"
        if baseline_t.get("unique_skill_id_count", 0) != current_t.get("unique_skill_id_count", 0):
            return "FAIL_CI"
        if baseline_t.get("schema_projection_sha256") != current_t.get("schema_projection_sha256"):
            return "FAIL_CI"
        if baseline_t.get("sha256") != current_t.get("sha256"):
            return "FAIL_CI"
    elif name == "hash_policy":
        if baseline_t.get("sha256") != current_t.get("sha256"):
            return "FAIL_CI"
        if baseline_t.get("hash_algorithm") != current_t.get("hash_algorithm"):
            return "FAIL_CI"
        if set(baseline_t.get("excluded_output_fields", [])) != set(current_t.get("excluded_output_fields", [])):
            return "FAIL_CI"
    elif name == "golden_hash_lock":
        if baseline_t.get("case_count", 0) != current_t.get("case_count", 0):
            return "FAIL_CI"
        if baseline_t.get("sha256") != current_t.get("sha256"):
            return "FAIL_CI"
    elif name == "golden_regression":
        bc = baseline_t.get("case_count", 0)
        cc = current_t.get("case_count", 0)
        bd = baseline_t.get("domains_covered", 0)
        cd = current_t.get("domains_covered", 0)

        # Count/domain checks first (before hash)
        if cc < bc:
            return "FAIL_CI"
        if cd < bd:
            return "FAIL_CI"
        if cc > bc or cd > bd:
            return "WARN"

        # Same count — content hash change is FAIL_CI
        if baseline_t.get("sha256") != current_t.get("sha256"):
            return "FAIL_CI"
    return "INFO"


def audit_semantic_drift() -> dict:
    baseline = load_baseline_snapshot()
    current = build_current_snapshot()
    return compare_snapshots(baseline, current)
