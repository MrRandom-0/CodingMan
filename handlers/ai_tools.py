# === handlers/ai_tools.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.ai import get_ai_response

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Please ask a question like this:\n/ask How to reverse a linked list?")
        return

    question = " ".join(context.args)
    prompt = f"Answer this programming question in simple words:\n{question}"
    response = await get_ai_response(prompt)
    await update.message.reply_text(f"🧠 *AI Answer:*\n{response}", parse_mode="Markdown")

ai_tools_handlers = [
    CommandHandler("ask", ask),
]
