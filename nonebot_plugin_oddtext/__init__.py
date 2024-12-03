import traceback

from nonebot import require
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Alconna, Args, on_alconna

from .data_source import Command, commands

__plugin_meta__ = PluginMetadata(
    name="文本生成器",
    description="抽象话等多种文本生成",
    usage=f"{'/'.join(sum([list(cmd.keywords) for cmd in commands], []))} + 文本",
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-oddtext",
    supported_adapters=None,
)


def create_matcher(command: Command):
    command_matcher = on_alconna(
        Alconna(command.keywords[0], Args["text", str]),
        aliases=set(command.keywords[1:]),
        block=True,
        priority=13,
        use_cmd_start=True,
    )

    @command_matcher.handle()
    async def _(matcher: Matcher, text: str):
        try:
            res = command.func(text)
        except Exception:
            logger.warning(traceback.format_exc())
            await matcher.finish("出错了，请稍后再试")
        await matcher.finish(res)


def create_matchers():
    for command in commands:
        create_matcher(command)


create_matchers()
