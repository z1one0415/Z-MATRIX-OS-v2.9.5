import ast, os
class TestNoProductionLinkage:
    def test_no_production(self):
        forbidden = {"broker","real_trade","production","order","account","credential","api_key","secret"}
        rt = "skillos/capability_invocation_os/runtime"
        for root, _, files in os.walk(rt):
            for fn in files:
                if fn.endswith(".py"):
                    with open(os.path.join(root, fn)) as fh:
                        tree = ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name.split(".")[0].lower() in forbidden:
                                    pytest.fail(f"{fn} imports {alias.name}")
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            if node.module.split(".")[0].lower() in forbidden:
                                pytest.fail(f"{fn} imports from {node.module}")
import pytest
