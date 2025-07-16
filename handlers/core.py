from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.ai import get_ai_response

# Global user state
user_prompts = {}
user_stats = {}
user_preferences = {
    "difficulty": {},  # uid -> 'easy' | 'medium' | 'hard'
    "language": {}     # uid -> 'Python' | 'Java' | ...
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to *Daily Coding Bot*!\nExplore coding problems, quizzes, interview prep, AI tools and more!",
        parse_mode="Markdown",
        reply_markup=main_menu_markup()
    )

# /today command
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_challenge(update, context)

# Generate and send challenge
async def send_challenge(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    uid = update_or_query.effective_user.id
    difficulty = user_preferences["difficulty"].get(uid, "medium")
    language = user_preferences["language"].get(uid, "Python")

    prompt = (
        f"Give a {difficulty} level programming challenge in {language}. "
        f"Only title and description. No hints or solution."
    )
    result = await get_ai_response(prompt)
    user_prompts[uid] = result
    user_stats.setdefault(uid, {"solved": 0, "streak": 0})

    # Buttons
    keyboard = [
        [InlineKeyboardButton("💡 Hint", callback_data="hint"),
         InlineKeyboardButton("✅ Solution", callback_data="solution")],
        [InlineKeyboardButton("🔁 New Challenge", callback_data="new_today")],
        [InlineKeyboardButton("📈 Progress", callback_data="progress"),
         InlineKeyboardButton("🔥 Streak", callback_data="streak")],
        [InlineKeyboardButton("🎯 Quiz", callback_data="quiz"),
         InlineKeyboardButton("🎤 Interview", callback_data="mockinterview")],
        [InlineKeyboardButton("⚙️ Difficulty", callback_data="difficulty"),
         InlineKeyboardButton("🧑‍💻 Language", callback_data="language")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="askai"),
         InlineKeyboardButton("📚 Bookmarks", callback_data="bookmarks")],
        [InlineKeyboardButton("🔧 Settings", callback_data="settings"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("📋 Main Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"🧠 *Today's Challenge:* (💬 {difficulty.title()} | 🧑‍💻 {language})\n\n```\n{result}\n```"

    if hasattr(update_or_query, "message"):  # from /today or /start
        await update_or_query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    elif hasattr(update_or_query, "edit_message_text"):  # from callback
        await update_or_query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=reply_markup)

# /menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 *Main Menu*", parse_mode="Markdown", reply_markup=main_menu_markup())

# Handle button callbacks
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    user_stats.setdefault(uid, {"solved": 0, "streak": 0})

    if query.data == "hint":
        if uid in user_prompts:
            prompt = f"Give a helpful hint for this problem:\n{user_prompts[uid]}"
            result = await get_ai_response(prompt)
            await query.message.reply_text(f"💡 *Hint:*\n{result}", parse_mode="Markdown")

    elif query.data == "solution":
        if uid in user_prompts:
            user_stats[uid]["solved"] += 1
            user_stats[uid]["streak"] += 1
            prompt = f"Give a Python solution with explanation:\n{user_prompts[uid]}"
            result = await get_ai_response(prompt)
            await query.message.reply_text(f"✅ *Solution:*\n{result}", parse_mode="Markdown")

    elif query.data == "new_today":
        await send_challenge(query, context)

    elif query.data == "progress":
        stats = user_stats[uid]
        await query.message.reply_text(
            f"📊 *Progress:*\nSolved: `{stats['solved']}`\n🔥 Streak: `{stats['streak']}`", parse_mode="Markdown"
        )

    elif query.data == "streak":
        await query.message.reply_text(f"🔥 *Current Streak:* {user_stats[uid]['streak']} day(s)", parse_mode="Markdown")

    elif query.data == "quiz":
        prompt = "Give a programming MCQ with 4 options and indicate the correct answer."
        result = await get_ai_response(prompt)
        await query.message.reply_text(f"🧠 *Quiz Time!*\n\n{result}", parse_mode="Markdown")

    elif query.data == "mockinterview":
        prompt = "Start a mock technical interview with one question."
        result = await get_ai_response(prompt)
        await query.message.reply_text(f"🎤 *Mock Interview Started:*\n\n{result}", parse_mode="Markdown")

    elif query.data == "askai":
        await query.message.reply_text("🤖 *Ask your coding question by typing:*\n/ask <your question>", parse_mode="Markdown")

    elif query.data == "bookmarks":
        await query.message.reply_text("📚 *You have no bookmarks yet.*\nUse /save to bookmark challenges.", parse_mode="Markdown")

    elif query.data == "settings":
        await query.message.reply_text("🔧 *Settings panel coming soon...*", parse_mode="Markdown")

    elif query.data == "profile":
        await query.message.reply_text("👤 *Your Profile:*\nXP: 300\nLevel: 4\nRank: #42", parse_mode="Markdown")

    elif query.data == "menu":
        await query.message.reply_text("📋 *Main Menu*", parse_mode="Markdown", reply_markup=main_menu_markup())

    elif query.data == "difficulty":
        await query.message.reply_text("⚙️ *Choose Difficulty:*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🟢 Easy", callback_data="set_difficulty_easy")],
            [InlineKeyboardButton("🟠 Medium", callback_data="set_difficulty_medium")],
            [InlineKeyboardButton("🔴 Hard", callback_data="set_difficulty_hard")],
        ]), parse_mode="Markdown")

    elif query.data.startswith("set_difficulty_"):
        level = query.data.replace("set_difficulty_", "")
        user_preferences["difficulty"][uid] = level
        await query.message.reply_text(f"✅ Difficulty set to *{level.capitalize()}*", parse_mode="Markdown")

    elif query.data == "language":
        await query.message.reply_text("💻 *Select Preferred Language:*", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🐍 Python", callback_data="lang_python")],
            [InlineKeyboardButton("☕ Java", callback_data="lang_java")],
            [InlineKeyboardButton("🔷 C++", callback_data="lang_cpp")],
            [InlineKeyboardButton("🌐 JavaScript", callback_data="lang_js")],
        ]), parse_mode="Markdown")

    elif query.data.startswith("lang_"):
        lang = query.data.replace("lang_", "").capitalize()
        user_preferences["language"][uid] = lang
        await query.message.reply_text(f"✅ Language preference set to *{lang}*", parse_mode="Markdown")

# Main menu layout
def main_menu_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Daily Challenge", callback_data="new_today")],
        [InlineKeyboardButton("📈 Progress", callback_data="progress"),
         InlineKeyboardButton("🔥 Streak", callback_data="streak")],
        [InlineKeyboardButton("🎯 Quiz", callback_data="quiz"),
         InlineKeyboardButton("🎤 Interview", callback_data="mockinterview")],
        [InlineKeyboardButton("⚙️ Difficulty", callback_data="difficulty"),
         InlineKeyboardButton("🧑‍💻 Language", callback_data="language")],
        [InlineKeyboardButton("🤖 Ask AI", callback_data="askai"),
         InlineKeyboardButton("📚 Bookmarks", callback_data="bookmarks")],
        [InlineKeyboardButton("🔧 Settings", callback_data="settings"),
         InlineKeyboardButton("👤 Profile", callback_data="profile")],
    ])

# Handler list
core_handlers = [
    CommandHandler("start", start),
    CommandHandler("today", today),
    CommandHandler("menu", menu),
    CallbackQueryHandler(button_handler),
]
