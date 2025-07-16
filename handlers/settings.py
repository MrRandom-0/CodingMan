# === handlers/settings.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

user_settings = {}

def get_user(uid):
    return user_settings.setdefault(uid, {"difficulty": "medium", "topic": "any"})

async def set_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: /set_difficulty <easy|medium|hard>")
        return
    level = context.args[0].lower()
    if level not in ["easy", "medium", "hard"]:
        await update.message.reply_text("⚠️ Invalid difficulty level. Choose from easy, medium, hard.")
        return
    get_user(update.effective_user.id)["difficulty"] = level
    await update.message.reply_text(f"✅ Difficulty set to *{level}*.", parse_mode="Markdown")

async def set_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗Usage: /set_topic <topic> (e.g., arrays, dp, strings)")
        return
    topic = context.args[0].lower()
    get_user(update.effective_user.id)["topic"] = topic
    await update.message.reply_text(f"📚 Topic preference set to *{topic}*.", parse_mode="Markdown")

settings_handlers = [
    CommandHandler("set_difficulty", set_difficulty),
    CommandHandler("set_topic", set_topic),
]
