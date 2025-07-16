# === daily_coding_bot/bot.py ===

import logging
from telegram.ext import ApplicationBuilder

from handlers.core import core_handlers
from handlers.ai_tools import ai_tools_handlers     # ✅ Fixed name
from handlers.quiz import quiz_handlers
from handlers.mock_interview import interview_handlers
from handlers.gamification import gamify_handlers   # ✅ Fixed name
from handlers.bookmarks import bookmark_handlers    # ✅ Added
from handlers.difficulty import difficulty_handlers # ✅ Added
from handlers.language import language_handlers     # ✅ Added
from handlers.profile import profile_handler        # ✅ Added
from handlers.reminder import reminder_handlers     # ✅ Added
from handlers.chat import chat_handler              # ✅ Fallback chat
from handlers.settings import settings_handlers
from handlers.core import core_handlers


from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register all grouped handlers
for handler_group in (
    core_handlers +
    ai_tools_handlers +
    quiz_handlers +
    interview_handlers +
    gamify_handlers +
    bookmark_handlers +
    difficulty_handlers +
    language_handlers +
    reminder_handlers +
    settings_handlers

):
    app.add_handler(handler_group)

# Register individual handler
app.add_handler(profile_handler)

# Fallback (chat-based AI)
app.add_handler(chat_handler)

# Run the bot
if __name__ == "__main__":
    print("🤖 Daily Coding Bot is running...")
    app.run_polling()
