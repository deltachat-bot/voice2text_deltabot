"""Event handlers and hooks."""

import logging
from argparse import Namespace

import whisper
from deltabot_cli import AttrDict, Bot, BotCli, EventType, const, events

cli = BotCli("voice2text-bot")
STATUS = "I am a Delta Chat bot, send me any voice message to convert it to text"
MODEL: whisper.Whisper = None  # noqa


@cli.on_init
async def on_init(bot: Bot, _args: Namespace) -> None:
    if not await bot.account.get_config("displayname"):
        await bot.account.set_config("displayname", "Voice To Text")
        await bot.account.set_config("selfstatus", STATUS)


@cli.on_start
async def on_start(_bot: Bot, _args: Namespace) -> None:
    global MODEL  # pylint: disable=W0603
    MODEL = whisper.load_model("medium")


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
        result = MODEL.transcribe(msg.file)
        await msg.chat.send_message(text=result["text"], quoted_msg=msg.id)
        return

    chat = await event.message_snapshot.chat.get_basic_snapshot()
    if chat.chat_type == const.ChatType.SINGLE:
        await event.message_snapshot.chat.send_message(
            text=STATUS, quoted_msg=event.message_snapshot.id
        )
