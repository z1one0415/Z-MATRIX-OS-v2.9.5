import ast, os, pytest
class TestP1NoProductionNoSideEffects:
    def test_no_production(self):
        forbidden={"broker","real_trade","production","order"}
        rt=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","..","..","skillos","capability_invocation_os","runtime")
        if not os.path.isdir(rt): pytest.skip("runtime dir not found")
        for root,_,files in os.walk(rt):
            for fn in files:
                if fn.endswith(".py"):
                    with open(os.path.join(root,fn)) as fh: tree=ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for a in node.names:
                                if a.name.split(".")[0].lower() in forbidden: pytest.fail(f"{fn} imports {a.name}")
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            if node.module.split(".")[0].lower() in forbidden: pytest.fail(f"{fn} from {node.module}")
    def test_no_runtime_enablement(self):
        rt=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","..","..","..","skillos","capability_invocation_os","runtime")
        if not os.path.isdir(rt): pytest.skip("runtime dir not found")
        with open(os.path.join(rt,"config.py")) as fh: content=fh.read()
        assert "runtime_enabled = True" not in content
        assert "adapter_execution_enabled = True" not in content
        assert "capability_execution_enabled = True" not in content
