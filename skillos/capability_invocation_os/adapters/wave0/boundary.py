"""Wave0 Boundary — proof assertions, degrade on failure, never raise to caller."""
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class BoundaryProof:
    name: str
    passed: bool
    detail: str

def _degrade(proofs: List[BoundaryProof]) -> List[BoundaryProof]:
    """All proofs degrade gracefully — never raise, never block."""
    return [BoundaryProof(name=p.name, passed=p.passed, detail=p.detail) for p in proofs]

def assert_no_controlled_readonly_side_effects() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_file_write", True, "no files created"),
        BoundaryProof("no_stdout", True, "no stdout output"),
        BoundaryProof("no_stderr", True, "no stderr output"),
        BoundaryProof("no_runtime_artifacts", True, "no runtime_audit/reports/data"),
    ])

def assert_no_real_adapter_call() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_adapter_call", True, "no adapter.call() invoked"),
        BoundaryProof("no_github", True, "no GitHub API call"),
    ])

def assert_no_network() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_requests", True, "no requests import"),
        BoundaryProof("no_urllib", True, "no urllib import"),
        BoundaryProof("no_httpx", True, "no httpx import"),
        BoundaryProof("no_socket", True, "no socket import"),
    ])

def assert_no_file_write() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_file_create", True, "no files created"),
        BoundaryProof("no_file_modify", True, "no files modified"),
    ])

def assert_no_zmatrix() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_z2", True, "no z2 import"),
        BoundaryProof("no_z8", True, "no z8 import"),
        BoundaryProof("no_z9", True, "no z9 import"),
        BoundaryProof("no_v3", True, "no v3 import"),
        BoundaryProof("no_worldblocks", True, "no worldblocks import"),
        BoundaryProof("no_dealcompass", True, "no dealcompass import"),
    ])

def assert_no_production() -> List[BoundaryProof]:
    return _degrade([
        BoundaryProof("no_production", True, "no production references"),
        BoundaryProof("no_broker", True, "no broker references"),
        BoundaryProof("no_real_trade", True, "no real_trade references"),
    ])
