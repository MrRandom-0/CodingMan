# === handlers/profile.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from handlers.core import user_stats
from utils.users import get_bookmarks, get_user_profile

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    profile = get_user_profile(uid)
    await update.message.reply_text(
        f"👤 *Your Profile:*\nXP: `{profile['xp']}`\nLevel: `{profile['level']}`\nRank: `{profile['rank']}`",
        parse_mode="Markdown"
    )

# /mystats — solved/streak + profile + bookmarks in one message
async def mystats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    profile = get_user_profile(uid)
    stats = user_stats.get(uid, {"solved": 0, "streak": 0})
    bookmark_count = len(get_bookmarks(uid))
    await update.message.reply_text(
        "📊 *Your Stats:*\n"
        f"✅ Solved: `{stats['solved']}`\n"
        f"🔥 Streak: `{stats['streak']}` day(s)\n"
        f"🎯 XP: `{profile['xp']}`\n"
        f"🏅 Level: `{profile['level']}`\n"
        f"🏆 Rank: `{profile['rank']}`\n"
        f"📚 Bookmarks: `{bookmark_count}`",
        parse_mode="Markdown"
    )

profile_handler = CommandHandler("profile", profile)
mystats_handler = CommandHandler("mystats", mystats)
