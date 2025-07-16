# === handlers/gamification.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Sample in-memory user XP data
user_xp_data = {}

def get_user_data(uid):
    if uid not in user_xp_data:
        user_xp_data[uid] = {"xp": 0, "level": 1, "rank": 999}
    return user_xp_data[uid]

# /xp - Show current XP
async def xp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user_data(uid)
    await update.message.reply_text(f"🎯 *You have:* `{user['xp']}` XP", parse_mode="Markdown")

# /level - Show current level
async def level_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user_data(uid)
    await update.message.reply_text(f"🏅 *Level:* `{user['level']}`", parse_mode="Markdown")

# /rank - Show (mock) global rank
async def rank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = get_user_data(uid)
    await update.message.reply_text(f"🏆 *Your Global Rank:* `#{user['rank']}`", parse_mode="Markdown")

# Exported handler list
gamify_handlers = [
    CommandHandler("xp", xp_command),
    CommandHandler("level", level_command),
    CommandHandler("rank", rank_command),
]
