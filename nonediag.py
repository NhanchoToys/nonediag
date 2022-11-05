from argparse import ArgumentParser
import os


def readlog():
    out = []
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
    ...


def readbotpy(fp: str):
    ...


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
    for base, _, files in os.walk(plugindir):
        for fi in files:
            if fi.endswith(".py"):
                with open(f"{base}/{fi}") as f:
                    try:
                        while True:
                            ln = f.readline()
                            if "from nonebot.adapters import" in ln \
                                    and any(x in ln for x in ("Message", "MessageEvent", "Bot")):
                                print("发现异常导入：" + ln)
                    except EOFError:
                        pass
    print(
        "解决方案：",
        "  请从正确的适配器（adapter）中导入相应对象",
        sep="\n"
    )


def main(args):
    log = readlog()
    print(log)
    if "ModuleNotFoundError" in log:
        lack_module(log)


if __name__ == "__main__":
    ap = ArgumentParser(
        "nonediag", description="NoneBot2 error diagnosing tool."
    )
    ap.add_argument("-B", "--botpy", nargs=1, default="./bot.py", help="specify bot.py dir")
    ap.add_argument("-v", "--venv", nargs=1, default=None, help="specify venv dir")
    args = ap.parse_args()
    print(args)
    main(args)
