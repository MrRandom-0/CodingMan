# === handlers/bookmarks.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.users import save_bookmark, get_bookmarks
from handlers.core import user_prompts

async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in user_prompts:
        save_bookmark(uid, user_prompts[uid])
        await update.message.reply_text("🔖 Challenge saved to bookmarks.")
    else:
        await update.message.reply_text("❗ No active challenge to save.")

async def bookmarks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    items = get_bookmarks(uid)
    if not items:
        await update.message.reply_text("📚 No bookmarks found.")
    else:
        formatted = "\n\n".join([f"🔹 {item}" for item in items[-5:]])
        await update.message.reply_text(f"📚 *Your Bookmarks (latest 5):*\n\n{formatted}", parse_mode="Markdown")

bookmark_handlers = [
    CommandHandler("save", save),
    CommandHandler("bookmarks", bookmarks),
]
