from argparse import ArgumentParser
from os import path
import os
import sys

from .versions import DEPRECATE_EXPORT, HAS_PLUGIN_JSON_TOML, HAS_PYTHON311, HAS_REQUIRE_EXPORT, NO_PYTHON37
from .models import duplicate_import, lack_module, no_export, not_implemented, port_used, warn_bad_import
from .base import noneversion, readlog, readbotpy, readtoml


def main(args):
    if sys.version_info < (3, 7):
        raise Exception("不受支持的 Python 版本，请使用更新版本 (>=3.7)")
    log = readlog()
    bothome: str = path.realpath(path.split(args.botfile)[0])
    os.chdir(bothome)
    if args.botfile.endswith(".toml"):
        info = {"adapters": [], "userload": [], "userload_builtin": []}
        info.update(readtoml(path.split(args.botfile)[1]))
    else:
        info = readbotpy(path.split(args.botfile)[1])
        info.update(readtoml(info["toml"]))
    print("[DEBUG]", info)
    # print(sys.path)
    
    if (nv := noneversion()) is not None:
        print("[DEBUG] Found nonebot2 version", nv)
        if sys.version_info >= (3, 11) and nv < HAS_PYTHON311:
            raise Exception(f"当前的 nonebot2 {nv} 还不支持更新的 Python，请使用更低版本的 Python (>=3.8,<3.11)")
        if sys.version_info < (3, 8) and nv >= NO_PYTHON37:
            raise Exception(f"当前的 nonebot2 {nv} 已不支持更旧的 Python，请使用更新版本的 Python (>=3.8)")
        if nv < HAS_REQUIRE_EXPORT or nv >= DEPRECATE_EXPORT:
            if "ImportError: cannot import name 'export' from 'nonebot'" in log:
                no_export(nv, info)
        if "RuntimeError: Plugin already exists: " in log:
            if nv >= HAS_PLUGIN_JSON_TOML:
                duplicate_import(log, info)
            else:
                print(
                    "警告：",
                    "  我们无法在当前版本下分析重复导入",
                    "  请自行排查 bot.py 中的重复导入",
                    "",
                    sep="\n"
                )
    if not info["adapters"]:
        print(
            "错误：",
            "  未找到可注册的适配器",
            "可能原因：",
            "  1. 使用 nb-cli 创建项目时未在适配器选择界面**按空格**选择需要的适配器",
            "  2. 使用了未识别的导入格式",
            "解决方案：",
            "  1. 使用 nb-cli 重新创建项目",
            "    nb create",
            "  2. 根据文档手动补全需要的适配器",
            "    nb adapter list",
            "    nb adapter install nonebot-adapter-xxx",
            "",
            sep="\n"
        )
    if info["userload"]:
        warn_bad_import(info["userload"])
    if "[Errno 10013]" in log:
        port_used()
    if "ModuleNotFoundError" in log:
        lack_module(log)
    if "NotImplementedError" in log:
        for d in info["plugin_dirs"]:
            not_implemented(d)


def _entry():
    ap = ArgumentParser(
        "nonediag", description="NoneBot2 error diagnosing tool."
    )
    ap.add_argument(
        "-B", "--botfile", nargs="?", default="./bot.py",
        help="specify bot.py or pyproject.toml dir"
    )
    args = ap.parse_args()
    # print(args)
    main(args)


if __name__ == "__main__":
    _entry()
