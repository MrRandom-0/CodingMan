# handlers/reminder.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, JobQueue

user_reminders = set()

async def remind_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_reminders.add(user_id)
    await update.message.reply_text("🔔 Daily reminder turned ON!")

async def remind_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_reminders.discard(user_id)
    await update.message.reply_text("🔕 Reminder turned OFF.")

async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    for uid in user_reminders:
        await context.bot.send_message(chat_id=uid, text="👋 Don't forget your daily challenge! Use /today")

reminder_handlers = [
    CommandHandler("remind", remind_on),
    CommandHandler("noremind", remind_off),
]
