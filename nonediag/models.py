import os
from shlex import quote
from typing import List

from nonediag.base import readpy
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


def no_export(ver):
    # covered
    print(
        "发现问题：",
        f"  'nonebot.export()' 需要满足依赖关系：nonebot2>={HAS_REQUIRE_EXPORT},<{REMOVE_EXPORT}",
        f"  当前 nonebot2 版本为 {ver}，不满足上述依赖要求",
        "解决方案：",
        "  1. 移除插件中的 'export'",
        f"  2. 升/降级 nonebot2 到上述依赖区间 (nonebot2>={HAS_REQUIRE_EXPORT},<{REMOVE_EXPORT})",
        "",
        sep="\n"
    )
