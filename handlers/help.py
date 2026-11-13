# === handlers/help.py ===

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
from utils.commands import format_help, format_unknown_command

# /help — list every command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(format_help(), parse_mode="Markdown")

# Any /command that matched nothing else (registered after all CommandHandlers)
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        format_unknown_command(update.message.text), parse_mode="Markdown"
    )

help_handler = CommandHandler("help", help_command)
unknown_command_handler = MessageHandler(filters.COMMAND, unknown_command)
