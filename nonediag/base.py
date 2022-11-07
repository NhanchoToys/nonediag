import ast
import tomlkit
from typing import List

from nonediag.deref import deref


def readlog():
    out: List[str] = []
    emptyline = 0
    try:
        while True:
            out.append(x := input())
            if not x:
                emptyline += 1
            else:
                emptyline = 0
            if emptyline > 2:
                break
    except EOFError:
        pass

    return "\n".join(out).strip()


def readtoml(fp: str):
    if not fp:
        return {"plugins": [], "plugin_dirs": []}
    with open(fp) as f:
        data = tomlkit.load(f)
    return {
        "plugins": data["tool"]["nonebot"]["plugins"],
        "plugin_dirs": data["tool"]["nonebot"]["plugin_dirs"]
    }


def readpy(fp: str):
    with open(fp, "rb") as f:
        return deref(f.read().decode(errors="ignore"))


def readbotpy(fp: str):
    out = {
        "adapters": [],
        "userload": [],
        "userload_builtin": [],
        "toml": ""
    }
    code, imp = readpy(fp)
    out["adapters"].extend(imp.values())
    for ln in code.splitlines():
        if "nonebot.load_from_toml" in ln:
            out["toml"] = ast.literal_eval(ln.split("nonebot.load_from_toml")[1])
        elif "nonebot.load_plugins" in ln:
            out["userload"].extend(ast.literal_eval(ln.split("nonebot.load_plugins")[1]))
        elif "nonebot.load_plugin" in ln:
            out["userload"].append(ast.literal_eval(ln.split("nonebot.load_plugin")[1]))
        elif "nonebot.load_builtin_plugins" in ln:
            out["userload_builtin"].extend(ast.literal_eval(ln.split("nonebot.load_builtin_plugins")[1]))
        elif "nonebot.load_builtin_plugin" in ln:
            out["userload_builtin"].append(ast.literal_eval(ln.split("nonebot.load_builtin_plugin")[1]))
    return out


def noneversion():
    from nonebot import VERSION
    return VERSION
