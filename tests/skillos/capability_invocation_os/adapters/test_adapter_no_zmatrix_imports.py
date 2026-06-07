import ast, os, pytest
class TestAdapterNoZmatrixImports:
    def test_no_zmatrix(self):
        forbidden={"z2","z8","z9","v3","worldblocks","dealcompass"}
        rt=os.path.join(os.path.dirname(__file__),"..","..","..","..","..","skillos","capability_invocation_os","adapters")
        if not os.path.isdir(rt): pytest.skip("adapters dir not resolved")
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
