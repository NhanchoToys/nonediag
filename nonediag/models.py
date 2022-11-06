import os
from shlex import quote
from typing import List

from nonediag.base import readpy


def lack_module(log: str):
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
        sep="\n"
    )


def not_implemented(plugindir: str):
    found = False
    for base, _, files in os.walk(plugindir):
        for fi in files:
            if fi.endswith(".py"):
                code, imp = readpy(f"{base}/{fi}")
                for x in ("Message", "MessageEvent", "Bot"):
                    if f"nonebot.adapters.{x}" in imp.values():
                        print(f"发现抽象基类：'nonebot.adapters.{x}'")
                        found = True
    if found:
        print(
            "解决方案：",
            "  请从正确的adapter （适配器）中导入相应对象",
            sep="\n"
        )


def warn_bad_import(imp: List[str]):
    print(
        "警告：",
        "  存在下列手动引入：",
        *("    " + quote(x) for x in imp),
        "建议：",
        "  请将插件导入尽可能写入 pyproject.toml",
        sep="\n"
    )
