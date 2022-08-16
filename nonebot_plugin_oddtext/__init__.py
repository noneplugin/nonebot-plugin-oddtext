import traceback
from nonebot import on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .data_source import commands, Command


__plugin_meta__ = PluginMetadata(
    name="多种文字生成",
    description="抽象话、火星文等文字生成",
    usage=("抽象话/火星文/蚂蚁文/翻转文字/故障文字 + 文本"),
    extra={
        "unique_name": "oddtext",
        "example": "抽象话 那真的牛逼",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.1.0",
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
