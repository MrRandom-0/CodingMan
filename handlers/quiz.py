# === handlers/quiz.py ===

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.ai import get_ai_response

# /quiz — fetch random programming MCQ
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "Give a random programming multiple choice question (MCQ) "
        "with 4 options labeled A, B, C, and D. "
        "Mark the correct answer clearly. "
        "Example:\n\n"
        "Question: What does 'len()' do in Python?\n"
        "A. Returns the number of items\n"
        "B. Adds items\n"
        "C. Deletes items\n"
        "D. Appends items\n"
        "Answer: A"
    )

    result = await get_ai_response(prompt)
    await update.message.reply_text(f"🎯 *Quiz Time!*\n\n{result}", parse_mode="Markdown")

quiz_handlers = [
    CommandHandler("quiz", quiz),
]
