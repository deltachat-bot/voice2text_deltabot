"""CLI subcommands"""
import logging
from argparse import Namespace

from deltabot_cli import Bot, BotCli

from .const import MODEL_CFG_KEY


def add_subcommands(cli: BotCli) -> None:
    cli.add_subcommand(model).add_argument(
        "model",
        help="set the whisper model to use, see https://github.com/openai/whisper/blob/main/model-card.md for possible values",
    )


async def model(bot: Bot, args: Namespace) -> None:
    await bot.account.set_config(MODEL_CFG_KEY, args.model)
    logging.info("model=%s", args.model)
