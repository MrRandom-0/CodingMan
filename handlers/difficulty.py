# handlers/difficulty.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.ai import get_ai_response

async def choose_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Easy", callback_data="diff_easy"),
         InlineKeyboardButton("🟡 Medium", callback_data="diff_medium"),
         InlineKeyboardButton("🔴 Hard", callback_data="diff_hard")]
    ]
    await update.message.reply_text("Choose difficulty level:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_difficulty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    difficulty = query.data.split("_")[1]
    prompt = f"Give a {difficulty} level coding challenge with only the title and description. No solution or hint."

    result = await get_ai_response(prompt)
    user_id = query.from_user.id
    context.bot_data[user_id] = {"last_prompt": result}

    await query.message.reply_text(f"🧠 *{difficulty.capitalize()} Challenge:*\n\n```\n{result}\n```", parse_mode="Markdown")

difficulty_handlers = [
    CommandHandler("difficulty", choose_difficulty),
    CallbackQueryHandler(handle_difficulty, pattern="^diff_"),
]
