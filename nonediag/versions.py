from pkg_resources import parse_version


def ALPHA(n: int, post: int = 0):
    """
    n: 1 ~ 16

    post: 0 ~ 2
    """
    return parse_version(f"2.0.0a{n}{f'.post{post}' if post > 0 else ''}")


def BETA(n: int):
    """n: 1 ~ 5"""
    return parse_version(f"2.0.0b{n}")


def RC(n: int):
    """n: 1 ~ ?"""
    return parse_version(f"2.0.0rc{n}")


def RELEASE(m: int = 0, n: int = 0):
    """m, n: greater than 0"""
    return parse_version(f"2.{m}.{n}")


HAS_REQUIRE_EXPORT = REMOVE_BUILTIN_APSCHEDULER = ALPHA(7)
HAS_APPROVE_REJECT = HAS_SHELLLIKE_COMMAND = ALPHA(9)
SPLITTED_ADAPTERS = HAS_PLUGIN_JSON_TOML = ALPHA(11)
HAS_CALLAPI = ALPHA(13, 1)
HAS_FORWARD_CONN = ALPHA(14)
HAS_MESSAGE_TEMPLATE = ALPHA(16)
NO_STRIPPED_EVENT = DEPRECATE_CQHTTP = DEPRECATE_TOML_NONEBOT_PLUGIN = BETA(1)
DEPRECATE_DEFAULT_STATE = HAS_LOAD_BUILTIN = BETA(2)
DEPRECATE_EXPORT = BETA(3)
HAS_PLUGIN_META = BETA(4)
HAS_MATCHER_EXPIRE = HAS_SYNCFUNC_START_STOP = BETA(5)
NO_PYTHON37 = REMOVE_DEFAULT_STATE = REMOVE_EXPORT = REMOVE_TOML_NONEBOT_PLUGIN = RC(1)
HAS_PYTHON311 = RC(2)
