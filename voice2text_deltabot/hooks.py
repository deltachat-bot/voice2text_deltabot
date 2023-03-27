"""Event handlers and hooks."""

import logging
from argparse import Namespace

from deltabot_cli import AttrDict, Bot, BotCli, EventType, const, events
from faster_whisper import WhisperModel

from .const import MODEL_CFG_KEY
from .subcommands import add_subcommands

cli = BotCli("voice2text-bot")
add_subcommands(cli)
STATUS = "I am a Delta Chat bot, send me any voice message to convert it to text"
MODEL: WhisperModel = None  # noqa


@cli.on_init
async def on_init(bot: Bot, _args: Namespace) -> None:
    if not await bot.account.get_config("displayname"):
        await bot.account.set_config("displayname", "Voice To Text")
        await bot.account.set_config("selfstatus", STATUS)


@cli.on_start
async def on_start(bot: Bot, _args: Namespace) -> None:
    global MODEL  # pylint: disable=W0603
    model = (await bot.account.get_config(MODEL_CFG_KEY)) or "medium"
    MODEL = WhisperModel(model, device="cpu", compute_type="int8")


@cli.on(events.RawEvent)
async def log_event(event: AttrDict) -> None:
    if event.type == EventType.INFO:
        logging.info(event.msg)
    elif event.type == EventType.WARNING:
        logging.warning(event.msg)
    elif event.type == EventType.ERROR:
        logging.error(event.msg)


@cli.on(events.NewMessage(is_info=False))
async def on_newmsg(event: AttrDict) -> None:
    msg = event.message_snapshot
    if msg.view_type in (const.ViewType.VOICE, const.ViewType.AUDIO):
        segments = MODEL.transcribe(msg.file)[0]
        result = "".join(segment.text for segment in segments)
        await msg.chat.send_message(text=result, quoted_msg=msg.id)
        return

    chat = await event.message_snapshot.chat.get_basic_snapshot()
    if chat.chat_type == const.ChatType.SINGLE:
        await event.message_snapshot.chat.send_message(
            text=STATUS, quoted_msg=event.message_snapshot.id
        )
