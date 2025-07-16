# handlers/language.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.ai import get_ai_response

async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🐍 Python", callback_data="lang_python"),
         InlineKeyboardButton("🟨 JavaScript", callback_data="lang_js"),
         InlineKeyboardButton("🧊 C++", callback_data="lang_cpp")]
    ]
    await update.message.reply_text("Choose a language for the solution:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.split("_")[1]
    user_id = query.from_user.id
    prompt = f"Give a {lang.upper()} solution with explanation for this coding challenge:\n{context.bot_data[user_id]['last_prompt']}"
    result = await get_ai_response(prompt)

    await query.message.reply_text(f"✅ *{lang.capitalize()} Solution:*\n{result}", parse_mode="Markdown")

language_handlers = [
    CommandHandler("language", choose_language),
    CallbackQueryHandler(handle_language, pattern="^lang_"),
]
