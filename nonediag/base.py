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
    out["adapters"].extend(x for x in imp.values() if x.startswith("nonebot.adapters."))
    for ln in code.splitlines():
        if "nonebot.load_from_toml" in ln:
            out["toml"] = ast.literal_eval(ln.split("nonebot.load_from_toml")[1])
        elif "nonebot.load_plugins" in ln:
            out["userload"].extend(ast.literal_eval(ln.split("nonebot.load_plugins")[1]))
        elif "nonebot.load_plugin" in ln:
            out["userload"].append(ast.literal_eval(ln.split("nonebot.load_plugin")[1]))
        elif "nonebot.load_builtin_plugins" in ln:
            data = ast.literal_eval(ln.split("nonebot.load_builtin_plugins")[1])
            out["userload_builtin"].append(data) if isinstance(data, str) else out["userload_builtin"].extend(data)
        elif "nonebot.load_builtin_plugin" in ln:
            out["userload_builtin"].append(ast.literal_eval(ln.split("nonebot.load_builtin_plugin")[1]))
    return out


def noneversion():
    try:
        from nonebot import VERSION
        return VERSION
    except (ImportError, ModuleNotFoundError):
        print(
            "警告：",
            "  **当前环境**没有 nonebot2",
            "  我们无法在缺少 nonebot2 的环境中进行详细诊断",
            "  您可能没有进入 bot 使用的环境",
            "解决方案：",
            "  1. 切换至有 nonebot2 的环境后运行本程序",
            "  2. 在当前环境安装 nonebot2",
            "",
            sep="\n"
        )
