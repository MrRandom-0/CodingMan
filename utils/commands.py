# === utils/commands.py ===
"""Single source of truth for the bot's command list.

Used to render /help and the unknown-command reply. This module is kept
free of telegram imports so it can be unit-tested on its own; a test
checks that every CommandHandler registered in handlers/ appears here.
"""

COMMAND_GROUPS = (
    ("Daily practice", (
        ("today", "Get today's coding challenge"),
        ("quiz", "Take a quick programming quiz"),
        ("mockinterview", "Start a mock technical interview"),
        ("remind", "Turn daily reminders on"),
        ("noremind", "Turn daily reminders off"),
    )),
    ("Your progress", (
        ("mystats", "Solved count, streak, XP, level and bookmarks in one place"),
        ("profile", "Show your profile (XP, level, rank)"),
        ("xp", "Show your XP"),
        ("level", "Show your level"),
        ("rank", "Show your rank"),
        ("bookmarks", "List your bookmarked challenges"),
    )),
    ("Preferences", (
        ("difficulty", "Choose challenge difficulty"),
        ("language", "Choose your programming language"),
        ("set_difficulty", "Set difficulty directly, e.g. /set_difficulty hard"),
        ("set_topic", "Set your preferred topic"),
        ("save", "Bookmark the current challenge"),
    )),
    ("AI & navigation", (
        ("ask", "Ask the AI a coding question, e.g. /ask what is a closure?"),
        ("menu", "Show the main menu"),
        ("start", "Show the welcome message and main menu"),
        ("help", "Show this help"),
    )),
)


def all_commands() -> tuple:
    """Every command name, in help order."""
    return tuple(name for _title, commands in COMMAND_GROUPS for name, _desc in commands)


def format_help() -> str:
    lines = ["❓ *CodingMan Help*", "Here is everything I can do:", ""]
    for title, commands in COMMAND_GROUPS:
        lines.append(f"*{title}*")
        for name, description in commands:
            lines.append(f"/{name} — {description}")
        lines.append("")
    lines.append("💬 You can also just type any coding question and I will answer it.")
    return "\n".join(lines).rstrip()


def format_unknown_command(text: str) -> str:
    """Friendly reply for a /command the bot does not recognise."""
    stripped = (text or "").strip()
    command = stripped.split()[0].split("@")[0] if stripped else "that command"
    return (
        f"🤔 I don't know `{command}` yet.\n"
        "Try /help to see everything I can do, or tap /menu for the main menu."
    )
