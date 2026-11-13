"""Tests for the command catalogue behind /help (utils/commands.py)."""

import re
from pathlib import Path

from utils.commands import all_commands, format_help, format_unknown_command

REPO_ROOT = Path(__file__).resolve().parent.parent


def registered_commands() -> set:
    """Every CommandHandler("name", ...) literal in handlers/ and bot.py."""
    names = set()
    sources = list((REPO_ROOT / "handlers").glob("*.py")) + [REPO_ROOT / "bot.py"]
    for source in sources:
        names.update(re.findall(r'CommandHandler\(\s*"([a-z_]+)"', source.read_text()))
    return names


def test_catalogue_has_no_duplicates():
    commands = all_commands()
    assert len(commands) == len(set(commands))


def test_help_lists_every_catalogued_command():
    help_text = format_help()
    for name in all_commands():
        assert f"/{name} " in help_text or f"/{name}\n" in help_text or f"/{name} —" in help_text


def test_help_covers_every_registered_handler():
    # If a command is added to a handler without updating the catalogue,
    # /help silently goes stale — fail loudly instead.
    assert registered_commands() <= set(all_commands())


def test_unknown_command_reply_names_command_and_points_to_help():
    reply = format_unknown_command("/frobnicate extra words")
    assert "/frobnicate" in reply
    assert "/help" in reply


def test_unknown_command_reply_handles_bot_suffix_and_empty():
    assert "/xyz" in format_unknown_command("/xyz@CodingManBot")
    assert "/help" in format_unknown_command("")
