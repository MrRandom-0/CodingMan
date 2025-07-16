# === handlers/chat.py ===

from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from utils.ai import get_ai_response

# 🧠 Catch-all handler for AI chat
async def fallback_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if not user_input:
        await update.message.reply_text("❗ Please enter a valid question or message.")
        return

    prompt = f"You are a friendly and knowledgeable AI coding assistant. Help with this:\n\n{user_input}"
    
    try:
        response = await get_ai_response(prompt)
        await update.message.reply_text(f"💬 *AI Says:*\n\n{response}", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Export as fallback handler (should be added LAST in bot.py)
chat_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_chat)
