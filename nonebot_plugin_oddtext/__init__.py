import traceback

from nonebot import on_command
from nonebot.adapters import Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_Handler

from .data_source import Command, commands

__plugin_meta__ = PluginMetadata(
    name="文本生成器",
    description="抽象话等多种文本生成",
    usage=f"{'/'.join(sum([list(command.keywords) for command in commands], []))} + 文本",
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-oddtext",
    supported_adapters=None,
    extra={
        "unique_name": "oddtext",
        "example": "抽象话 那真的牛逼",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.2.0",
    },
)


def create_matchers():
    def create_handler(command: Command) -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            text = msg.extract_plain_text().strip()
            if not text:
                matcher.block = False
                await matcher.finish()
            try:
                res = command.func(text)
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("出错了，请稍后再试")
            await matcher.finish(res)

        return handler

    for command in commands:
        on_command(
            command.keywords[0], aliases=set(command.keywords), block=True, priority=13
        ).append_handler(create_handler(command))


create_matchers()
