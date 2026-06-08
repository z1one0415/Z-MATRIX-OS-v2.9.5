import pytest, os

WAVE0_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'skillos', 'capability_invocation_os', 'adapters', 'wave0')
FORBIDDEN = ['requests', 'urllib', 'httpx', 'socket', 'z2', 'z8', 'z9', 'v3', 'worldblocks', 'dealcompass']

def _get_files():
    if not os.path.isdir(WAVE0_DIR): return []
    return [os.path.join(WAVE0_DIR, f) for f in os.listdir(WAVE0_DIR) if f.endswith('.py') and not f.startswith('__')]

def test_no_forbidden_imports():
    for fpath in _get_files():
        with open(fpath) as f:
            content = f.read()
        for forbidden in FORBIDDEN:
            if f"import {forbidden}" in content or f"from {forbidden}" in content:
                if 'FORBIDDEN' not in content.split(f"import {forbidden}")[0].split('\n')[-1]:
                    assert False, f"Forbidden import '{forbidden}' in {fpath}"
