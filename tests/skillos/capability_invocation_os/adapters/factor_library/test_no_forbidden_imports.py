import pytest, os

FACTOR_LIB_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..',
                              'skillos', 'capability_invocation_os', 'adapters', 'factor_library')

FORBIDDEN = ['requests', 'urllib', 'httpx', 'socket', 'z2', 'z8', 'z9', 'v3',
             'worldblocks', 'dealcompass', 'broker', 'trading', 'execution',
             'runtime_reports', 'research.factor_library']

def test_no_forbidden_imports_in_adapters():
    if not os.path.isdir(FACTOR_LIB_DIR): pytest.skip()
    for fname in os.listdir(FACTOR_LIB_DIR):
        if not fname.endswith('.py') or fname.startswith('__'): continue
        fpath = os.path.join(FACTOR_LIB_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        for fb in FORBIDDEN:
            if f"import {fb}" in content or f"from {fb}" in content:
                if 'FORBIDDEN' not in content.split(f"import {fb}")[0].split('\n')[-1]:
                    assert False, f"'{fb}' imported in {fname}"
