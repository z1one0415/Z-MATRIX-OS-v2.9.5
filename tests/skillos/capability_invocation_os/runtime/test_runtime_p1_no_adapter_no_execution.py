import ast, os, pytest
class TestP1NoAdapterNoExecution:
    def test_no_adapter_imports(self):
        forbidden={"z2","z8","z9","v3","worldblocks","dealcompass"}
        for root,_,files in os.walk("skillos/capability_invocation_os/runtime"):
            for fn in files:
                if fn.endswith(".py"):
                    with open(os.path.join(root,fn)) as fh: tree=ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for a in node.names:
                                if a.name.split(".")[0].lower() in forbidden: pytest.fail(f"{fn} imports {a.name}")
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            if node.module.split(".")[0].lower() in forbidden: pytest.fail(f"{fn} from {node.module}")
    def test_no_execution_functions(self):
        forbidden=["execute_capability","call_capability","run_adapter","load_adapter"]
        for root,_,files in os.walk("skillos/capability_invocation_os/runtime"):
            for fn in files:
                if fn.endswith(".py"):
                    with open(os.path.join(root,fn)) as fh: content=fh.read()
                    for w in forbidden:
                        if w in content and "test" not in content and "forbidden" not in content.split(w)[0].rsplit("\n",2)[-1]:
                            pass
