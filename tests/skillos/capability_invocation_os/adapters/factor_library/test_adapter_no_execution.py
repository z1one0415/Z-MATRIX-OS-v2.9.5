import pytest
import inspect
from skillos.capability_invocation_os.adapters.factor_library.adapter import FactorLibraryReadOnlyAdapter
from skillos.capability_invocation_os.adapters.factor_library.constants import FORBIDDEN_METHOD_NAMES

def test_no_execute_method():
    methods = [m for m in dir(FactorLibraryReadOnlyAdapter) if not m.startswith('_')]
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"Forbidden method '{forbidden}' found on adapter"

def test_forbidden_imports_not_present():
    import ast, os
    adapter_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..',
                                'skillos', 'capability_invocation_os', 'adapters', 'factor_library', 'adapter.py')
    with open(adapter_path) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = getattr(node, 'module', '') or ''
            for name in [module] + [a.name for a in node.names]:
                assert 'research' not in name, f"Forbidden import '{name}' in adapter.py"
                assert 'zmatrix' not in name.lower()
                assert 'runtime_reports' not in name
                assert 'broker' not in name.lower()
                assert 'trading' not in name.lower()
