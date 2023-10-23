"""CLI subcommands"""
import logging
from argparse import Namespace

from deltabot_cli import Bot, BotCli

from .const import MODEL_CFG_KEY


def add_subcommands(cli: BotCli) -> None:
    cli.add_subcommand(model).add_argument(
        "model",
        help="the whisper model, for possible values see https://github.com/openai/whisper/blob/main/model-card.md",
    )


def model(bot: Bot, args: Namespace) -> None:
    """set the whisper model to use"""
    bot.account.set_config(MODEL_CFG_KEY, args.model)
    logging.info("model=%s", args.model)
