# === handlers/profile.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.users import get_user_profile

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    profile = get_user_profile(uid)
    await update.message.reply_text(
        f"👤 *Your Profile:*\nXP: `{profile['xp']}`\nLevel: `{profile['level']}`\nRank: `{profile['rank']}`",
        parse_mode="Markdown"
    )

profile_handler = CommandHandler("profile", profile)
