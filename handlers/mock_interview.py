# === handlers/mock_interview.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.ai import get_ai_response

# /mockinterview — start mock interview
async def mock_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "Start a mock technical interview for a software developer. "
        "Ask one interview-style programming or system design question with context. "
        "Don’t provide an answer unless asked."
    )
    result = await get_ai_response(prompt)
    await update.message.reply_text(f"🎤 *Mock Interview Started:*\n\n{result}", parse_mode="Markdown")

interview_handlers = [
    CommandHandler("mockinterview", mock_interview),
]
