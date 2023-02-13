# Voice To Text Bot

[![CI](https://github.com/deltachat-bot/voice2text_deltabot/actions/workflows/python-ci.yml/badge.svg)](https://github.com/deltachat-bot/voice2text_deltabot/actions/workflows/python-ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A voice-to-text converter bot for Delta Chat.

## Install

```sh
pip install git+https://github.com/deltachat-bot/voice2text-deltabot.git
```

The bot uses [Whisper](https://github.com/openai/whisper) to extract the text from voice messages,
Whisper requires the command-line tool `ffmpeg` to be installed on your system, which is available
from most package managers:

```sh
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg
```

### Installing deltachat-rpc-server

This program depends on a standalone Delta Chat RPC server `deltachat-rpc-server` program that must be
available in your `PATH`. To install it check:
https://github.com/deltachat/deltachat-core-rust/tree/master/deltachat-rpc-server

## Usage

To configure the bot:

```sh
voice2text-bot init bot@example.org SuperHardPassword
```

To customize the bot name, avatar and status/signature:

```sh
voice2text-bot set_avatar "/path/to/avatar.png"
voice2text-bot config displayname "Voice To Text"
voice2text-bot config selfstatus "Hi, send me some voice message to convert it to text"
```

Finally you can start the bot with:

```sh
voice2text-bot
```

To see the available options, run in the command line:

```
voice2text-bot --help
```

**Note:** You can also run the bot CLI with `python -m voice2text-deltabot`
