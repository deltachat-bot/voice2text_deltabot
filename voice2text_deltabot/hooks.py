"""Event handlers and hooks."""

import time
from argparse import Namespace

from deltabot_cli import AttrDict, Bot, BotCli, ChatType, EventType, ViewType, events
from faster_whisper import WhisperModel
from rich.logging import RichHandler

cli = BotCli("voice2text-bot")
cli.add_generic_option(
    "--no-time",
    help="do not display date timestamp in log messages",
    action="store_false",
)
cli.add_generic_option(
    "--model",
    help="set the whisper model to use, for example: small, medium, large. (default: %(default)s)",
    default="large",
)
cli.add_generic_option(
    "--compute-type",
    help="set the compute type (default: %(default)s)",
    choices=["int8", "float16", "int8_float16"],
    default="int8",
)
STATUS = "I'm a Delta Chat bot, send me any voice message to convert it to text"
MODEL: WhisperModel = None  # noqa


@cli.on_init
def _on_init(bot: Bot, args: Namespace) -> None:
    bot.logger.handlers = [
        RichHandler(show_path=False, omit_repeated_times=False, show_time=args.no_time)
    ]
    for accid in bot.rpc.get_all_account_ids():
        if not bot.rpc.get_config(accid, "displayname"):
            bot.rpc.set_config(accid, "displayname", "Voice To Text")
            bot.rpc.set_config(accid, "selfstatus", STATUS)
            bot.rpc.set_config(accid, "delete_server_after", "1")
            bot.rpc.set_config(accid, "delete_device_after", str(60 * 60 * 24))


@cli.on_start
def on_start(_bot: Bot, args: Namespace) -> None:
    global MODEL  # pylint: disable=W0603
    MODEL = WhisperModel(args.model, device="auto", compute_type=args.compute_type)


@cli.on(events.RawEvent)
def _log_event(bot: Bot, accid: int, event: AttrDict) -> None:
    if event.kind == EventType.INFO:
        bot.logger.debug(event.msg)
    elif event.kind == EventType.WARNING:
        bot.logger.warning(event.msg)
    elif event.kind == EventType.ERROR:
        bot.logger.error(event.msg)
    elif event.kind == EventType.SECUREJOIN_INVITER_PROGRESS:
        if event.progress == 1000:
            bot.logger.debug("QR scanned by contact id=%s", event.contact_id)
            chatid = bot.rpc.create_chat_by_contact_id(accid, event.contact_id)
            bot.rpc.send_msg(accid, chatid, {"text": STATUS})


@cli.on(events.NewMessage(is_info=False, is_bot=None))
def on_newmsg(bot: Bot, accid: int, event: AttrDict) -> None:
    msg = event.msg
    chat = bot.rpc.get_basic_chat_info(accid, msg.chat_id)
    if chat.chat_type == ChatType.SINGLE:
        bot.rpc.markseen_msgs(accid, [msg.id])
        if msg.is_bot:
            return

    if msg.view_type in (ViewType.VOICE, ViewType.AUDIO):
        start = time.time()
        segments, info = MODEL.transcribe(msg.file)
        text = " ".join(seg.text for seg in segments)
        took = time.time() - start
        percent = int(info.language_probability * 100)
        bot.logger.info(
            f"[chat={msg.chat_id}, msg={msg.id}] Voice extracted: lang={info.language}"
            f" (probability={percent}%) took {took:.1f} seconds"
        )
        bot.rpc.send_msg(accid, msg.chat_id, {"text": text, "quotedMessageId": msg.id})
    elif chat.chat_type == ChatType.SINGLE:
        bot.rpc.send_msg(accid, msg.chat_id, {"text": STATUS})
