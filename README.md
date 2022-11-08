# nonediag

NoneBot2 error diagnosing tool.

NoneBot2 错误诊断工具。

## Supported Function | 支持功能

nonediag 目前支持以下类型的错误诊断：

- 模块/适配器缺失
- Python 版本不适配
- 错误导入抽象基类
- bot.py 手动导入检查及重复导入
- `nonebot.export` 和 `nonebot.params.State` 检查
- 端口占用提示

## Installation | 安装

在 bot 环境中安装 nonediag

```console
pip install nonediag
```

## Usage | 使用

1. 在命令行中输入下列指令：

    ```console
    cd /path/to/bot
    nonediag
    ```

2. 输入你的错误信息；
3. 输入完成后敲入 3-4 个换行即可。
