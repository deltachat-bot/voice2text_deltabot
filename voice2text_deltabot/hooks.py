"""Event handlers and hooks."""

import logging
from argparse import Namespace

import whisper
from deltabot_cli import AttrDict, Bot, BotCli, EventType, const, events

from .const import MODEL_CFG_KEY
from .subcommands import add_subcommands

cli = BotCli("voice2text-bot")
add_subcommands(cli)
STATUS = "I am a Delta Chat bot, send me any voice message to convert it to text"
MODEL: whisper.Whisper = None  # noqa


@cli.on_init
def on_init(bot: Bot, _args: Namespace) -> None:
    if not bot.account.get_config("displayname"):
        bot.account.set_config("displayname", "Voice To Text")
        bot.account.set_config("selfstatus", STATUS)


@cli.on_start
def on_start(bot: Bot, _args: Namespace) -> None:
    global MODEL  # pylint: disable=W0603
    model = bot.account.get_config(MODEL_CFG_KEY) or "medium"
    MODEL = whisper.load_model(model)


@cli.on(events.RawEvent)
def log_event(event: AttrDict) -> None:
    if event.type == EventType.INFO:
        logging.info(event.msg)
    elif event.type == EventType.WARNING:
        logging.warning(event.msg)
    elif event.type == EventType.ERROR:
        logging.error(event.msg)


@cli.on(events.NewMessage(is_info=False))
def on_newmsg(event: AttrDict) -> None:
    msg = event.message_snapshot
    if msg.view_type in (const.ViewType.VOICE, const.ViewType.AUDIO):
        result = MODEL.transcribe(msg.file)
        msg.chat.send_message(text=result["text"], quoted_msg=msg.id)
        return

    chat = event.message_snapshot.chat.get_basic_snapshot()
    if chat.chat_type == const.ChatType.SINGLE:
        event.message_snapshot.chat.send_message(
            text=STATUS, quoted_msg=event.message_snapshot.id
        )
