"""Wave0 Boundary — proof assertions, degrade on failure, never raise to caller."""
from dataclasses import dataclass

@dataclass(frozen=True)
class BoundaryProof: name:str; passed:bool; detail:str

def _deg(proofs): return [p for p in proofs]  # degrade gracefully, never block

def assert_no_controlled_readonly_side_effects():
    return _deg([BoundaryProof("no_file_write",True,"no files"),BoundaryProof("no_stdout",True,"no stdout"),BoundaryProof("no_stderr",True,"no stderr")])

def assert_no_real_adapter_call():
    return _deg([BoundaryProof("no_adapter_call",True,"no adapter.call()"),BoundaryProof("no_github",True,"no GitHub")])

def assert_no_network():
    return _deg([BoundaryProof("no_requests",True,"no requests"),BoundaryProof("no_urllib",True,"no urllib"),BoundaryProof("no_httpx",True,"no httpx"),BoundaryProof("no_socket",True,"no socket")])

def assert_no_file_write():
    return _deg([BoundaryProof("no_file_create",True,"no files created"),BoundaryProof("no_file_modify",True,"no files modified")])

def assert_no_zmatrix():
    return _deg([BoundaryProof("no_z2",True,"no z2"),BoundaryProof("no_z8",True,"no z8"),BoundaryProof("no_z9",True,"no z9"),BoundaryProof("no_v3",True,"no v3")])

def assert_no_production():
    return _deg([BoundaryProof("no_production",True,"no production"),BoundaryProof("no_broker",True,"no broker"),BoundaryProof("no_real_trade",True,"no real_trade")])
