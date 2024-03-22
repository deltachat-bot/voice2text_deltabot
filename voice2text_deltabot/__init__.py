"""Voice-to-text converter bot"""

from .hooks import cli


def main() -> None:
    """Start the CLI application."""
    try:
        cli.start()
    except KeyboardInterrupt:
        pass
