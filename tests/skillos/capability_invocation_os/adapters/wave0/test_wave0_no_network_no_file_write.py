import ast,os
class TestNoNetwork:
    def test_no_requests(self):
        forbidden={"requests","urllib","httpx","socket","http"}
        rt=os.path.join(os.path.dirname(__file__),"..","..","..","..","..","skillos","capability_invocation_os","adapters","wave0")
        if not os.path.isdir(rt): return
        for r,_,fs in os.walk(rt):
            for fn in fs:
                if fn.endswith(".py"):
                    with open(os.path.join(r,fn)) as fh: tree=ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node,ast.Import):
                            for a in node.names:
                                if a.name.split(".")[0].lower() in forbidden: raise AssertionError(f"{fn} imports {a.name}")
                        elif isinstance(node,ast.ImportFrom) and node.module:
                            if node.module.split(".")[0].lower() in forbidden: raise AssertionError(f"{fn} from {node.module}")
    def test_no_file_ops(self):
        forbidden={"open","write","remove","mkdir","shutil"}
        rt=os.path.join(os.path.dirname(__file__),"..","..","..","..","..","skillos","capability_invocation_os","adapters","wave0")
        if not os.path.isdir(rt): return
