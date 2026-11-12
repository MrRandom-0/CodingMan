# CodingMan

A Telegram bot for daily coding practice. CodingMan sends coding challenges, runs quizzes and mock interviews, and keeps learners on streaks with reminders and light gamification — all inside Telegram.

## Features

- **Daily challenges & quizzes** — coding questions by difficulty level and programming language
- **Mock interviews** — interview-style practice sessions in chat
- **AI tools** — AI-assisted help powered by OpenRouter
- **Gamification** — points and streaks to keep the daily habit going
- **Bookmarks** — save questions to revisit later
- **Reminders** — scheduled nudges so a day is never missed
- **Profiles & settings** — per-user language, difficulty and preferences

## Requirements

- Python 3.10+ (see `runtime.txt`)
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- An [OpenRouter](https://openrouter.ai) API key for the AI features

## Setup

```bash
git clone https://github.com/MrRandom-0/CodingMan.git
cd CodingMan
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in your keys
python bot.py
```

## Configuration

All configuration is via environment variables (loaded from `.env` by `config.py`). The bot refuses to start if a required variable is missing.

| Variable | Required | Purpose |
| --- | --- | --- |
| `BOT_TOKEN` | Yes | Telegram bot token from BotFather |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key for AI features |

Never commit your `.env` — it is already listed in `.gitignore`.

## Project layout

```
bot.py          Entry point — builds the app and registers all handler groups
config.py       Environment-based configuration (fails fast when keys are missing)
handlers/       One module per feature (quiz, mock interview, AI tools,
                gamification, bookmarks, reminders, difficulty, language,
                profile, settings, core commands, chat fallback)
utils/          Question loading and user-store helpers
data/           Question bank (questions.json) and the user store (user.json)
```

## Status

Personal learning project, maintained as time permits. Issues and pull requests are welcome.
