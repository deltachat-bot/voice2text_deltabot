# Voice To Text Bot

[![Latest Release](https://img.shields.io/pypi/v/voice2text-deltabot.svg)](https://pypi.org/project/voice2text-deltabot)
[![CI](https://github.com/deltachat-bot/voice2text_deltabot/actions/workflows/python-ci.yml/badge.svg)](https://github.com/deltachat-bot/voice2text_deltabot/actions/workflows/python-ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A voice-to-text converter bot for Delta Chat.

## Install

```sh
pip install voice2text-deltabot
```

The bot uses [Faster Whisper](https://github.com/guillaumekln/faster-whisper/) to extract the text
from voice messages.

## Usage

To configure the bot:

```sh
voice2text-bot init bot@example.org SuperHardPassword
```

**(Optional)** To customize the bot name, avatar and status/signature:

```sh
voice2text-bot config selfavatar "/path/to/avatar.png"
voice2text-bot config displayname "Voice To Text"
voice2text-bot config selfstatus "Hi, send me some voice message to convert it to text"
```

Finally you can start the bot with:

```sh
voice2text-bot serve
```

To see the available options, run in the command line:

```
voice2text-bot --help
```
