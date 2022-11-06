from argparse import ArgumentParser
from os import path
import os

from .models import lack_module, not_implemented, warn_bad_import
from .base import readlog, readbotpy, readtoml


def main(args):
    log = readlog()
    bothome: str = path.realpath(path.split(args.botfile)[0])
    os.chdir(bothome)
    if args.botfile.endswith(".toml"):
        info = {"adapters": [], "userload": []}
        plugin = readtoml(path.split(args.botfile)[1])
    else:
        info = readbotpy(path.split(args.botfile)[1])
        plugin = readtoml(info["toml"])
    print(info, plugin)
    if info["userload"]:
        warn_bad_import(info["userload"])
    if "ModuleNotFoundError" in log:
        lack_module(log)
    if "NotImplementedError" in log:
        for d in plugin["plugin_dirs"]:
            not_implemented(d)


if __name__ == "__main__":
    ap = ArgumentParser(
        "nonediag", description="NoneBot2 error diagnosing tool."
    )
    ap.add_argument(
        "-B", "--botfile", nargs="?", default="./bot.py",
        help="specify bot.py or pyproject.toml dir"
    )
    args = ap.parse_args()
    print(args)
    main(args)
