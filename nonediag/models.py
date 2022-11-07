import os
from shlex import quote
import sys
from typing import List
import zipfile

from nonediag.base import readpy
from nonediag.deref import deref
from nonediag.versions import HAS_REQUIRE_EXPORT, REMOVE_EXPORT


def lack_module(log: str):
    # covered
    for ln in log.splitlines():
        if ln.startswith("ModuleNotFoundError"):
            print(
                "发现错误信息：" + ln,
                f"可能原因：**当前环境**未安装 {ln.split(' ')[-1]}",
                sep="\n"
            )
    print(
        "解决方案：",
        "  1. 检查运行 bot 的环境并更换至正确的环境",
        "  2. 通过 pip / nb 补全相关依赖",
        "\n",
        sep=""
    )


def not_implemented(plugindir: str):
    found = False
    for base, _, files in os.walk(plugindir):
        for fi in files:
            if fi.endswith(".py"):
                code, imp = readpy(f"{base}/{fi}")
                for x in ("Message", "MessageEvent", "Bot"):
                    if f"nonebot.adapters.{x}" in imp.values():
                        print(f"发现抽象基类：'nonebot.adapters.{x}' ({base}/{fi})")
                        found = True
    if found:
        print(
            "解决方案：",
            "  请从正确的adapter（适配器）中导入相应对象",
            "\n",
            sep=""
        )


def warn_bad_import(imp: List[str]):
    # covered
    print(
        "警告：",
        "  存在下列手动导入：",
        *("    " + quote(x) for x in imp),
        "建议：",
        "  请将插件导入尽可能写入 pyproject.toml",
        "",
        sep="\n"
    )


def duplicate_import(log: str, data):
    # covered
    found = []
    for ln in log.splitlines():
        if ln.startswith("RuntimeError: Plugin already exists: "):
            found.append(x := ln.split('!', 1)[0][37:])
            print(f"发现重复导入：{x!r}")
    if found:
        for pl in found:
            if pl in data["plugins"]:
                print(f"插件 {pl!r} 已经在 toml 中加载")
                print("  请在 bot.py 中移除相关导入")
        print()


def _zip_ls(zip: str):
    with zipfile.ZipFile(zip) as f:
        return [x.filename for x in f.filelist]


def _zip_view(zip: str, fp: str):
    with zipfile.ZipFile(zip) as f:
        return f.open(fp).read()


def no_export(ver, info):
    # covered
    found = []
    for upld in info["plugin_dirs"]:
        for base, _, fns in os.walk(upld):
            for fn in fns:
                if fn.endswith(".py"):
                    c, imp = readpy(f"{base}/{fn}")
                    if "nonebot.export(" in c or "nonebot.export" in imp.values():
                        found.append(f"{base}/{fn}")

    for p in sys.path[::-1]:
        # if found:
        #     break
        try:
            if p.endswith(".zip"):
                for fp in _zip_ls(p):
                    if fp.endswith(".py"):
                        precode = _zip_view(p, fp).decode()
                        code, imp = deref(precode)
                        if "nonebot.export(" in code or "nonebot.export" in imp.values():
                            found.append(f"{p}#{fp}")
            else:
                for base, _, fns in os.walk(p):
                    if "nonebot_plugin" not in base:
                        continue
                    for fn in fns:
                        if fn.endswith(".py"):
                            # print(f"Looking up {base}/{fn} ...")
                            c, imp = readpy(f"{base}/{fn}")
                            if "nonebot.export(" in c or "nonebot.export" in imp.values():
                                found.append(f"{base}/{fn}")
        except FileNotFoundError:
            pass

    print(
        "发现问题：",
        f"  'nonebot.export()' 需要满足依赖关系：nonebot2>={HAS_REQUIRE_EXPORT},<{REMOVE_EXPORT}",
        f"  当前 nonebot2 版本为 {ver}，不满足上述依赖要求",
        "已找到使用 'nonebot.export()' 的文件：",
        *("  " + d for d in found),
        "解决方案：",
        "  1. 移除插件中的 'export'",
        "  2. 升/降级 nonebot2 到上述依赖区间",
        "",
        sep="\n"
    )


def port_used():
    print(
        "发现错误：端口被占用",
        "解决方案：",
        "  修改环境文件（.env*）中的 PORT 为其他值",
        sep="\n"
    )
