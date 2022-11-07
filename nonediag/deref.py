import ast
import os
from typing import Dict
from importlib.util import resolve_name


def makeattr(name: str):
    if "." in name:
        next, attr = name.rsplit(".", 1)
    else:
        next, attr = None, name
    if next is not None:
        return ast.Attribute(makeattr(next), attr, ctx=ast.Load())
    return ast.Name(attr, ctx=ast.Load())


class Normalizer(ast.NodeTransformer):
    def __init__(self, refs) -> None:
        self.__name_refs = refs
        super().__init__()

    def visit_Import(self, node):
        return None

    visit_ImportFrom = visit_Import

    def visit_Name(self, node):
        if node.ctx != ast.Load():
            return node
        return node if node.id not in self.__name_refs else makeattr(self.__name_refs[node.id])


class RefSys:
    def __init__(self) -> None:
        self.refs: Dict[str, str] = {}
        self.package = os.curdir

    def solveattr(self, o):
        if not isinstance(o, ast.Attribute):
            raise ValueError("Expecting ast.Attribute")
        if isinstance(o.value, ast.Attribute):
            return f"{self.solveattr(o.value)}.{o.attr}"
        if isinstance(o.value, ast.Call):
            return f"{ast.unparse(o.value)}.{o.attr}"
        return f"{self.solveref(o.value.id)}.{o.attr}"

    def createref(self, o):
        if isinstance(o, ast.Import):
            self.refs.update({x.asname: x.name for x in o.names if x.asname is not None})
            return True
        elif isinstance(o, ast.ImportFrom):
            try:
                self.refs.update(
                    {
                        (x.asname if x.asname is not None else x.name): resolve_name("." * o.level + ".".join((o.module, x.name) if o.module is not None else (x.name, )), self.package)
                        for x in o.names
                    }
                )
                return True
            except ImportError:
                return False
        elif isinstance(o, ast.Assign):
            if isinstance((t := o.targets[0]), ast.Tuple):
                if not isinstance(o.value, ast.Tuple):
                    return False
                self.refs.update(p := {k.id: v.id for k, v in zip(t.elts, o.value.elts) if isinstance(k, ast.Name) and isinstance(v, ast.Name)})
            elif isinstance(t, (ast.Subscript, ast.Attribute)) or isinstance(o.value, (ast.Subscript, ast.Attribute)):
                return False
            else:
                self.refs.update(p := {t.id: o.value.id} if isinstance(t, ast.Name) and isinstance(o.value, ast.Name) else {t.id: self.solveattr(o.value)} if isinstance(t, ast.Name) and isinstance(o.value, ast.Attribute) else {})
            return bool(p)
        else:
            raise ValueError("Expecting ast.Import, ast.ImportFrom or ast.Assign")

    def solveref(self, name: str):
        while name in self.refs:
            name = self.refs[name]
        return name


def deref(code: str):
    ref = RefSys()
    parsed = ast.parse(code)
    for o in ast.walk(parsed):
        if isinstance(o, (ast.Import, ast.ImportFrom, ast.Assign)):
            ref.createref(o)
            continue
        # print(ast.dump(o))
        # print()

    # for x in parsed:
    parsed = Normalizer(ref.refs).visit(parsed)
    out = ast.unparse(parsed)
    # print(out := ast.unparse(parsed))
    # print(ref.refs)
    return out, ref.refs
