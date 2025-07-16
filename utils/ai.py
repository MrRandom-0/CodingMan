# utils/ai.py

import aiohttp
from config import OPENROUTER_API_KEY

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"  # or other free model

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

async def get_ai_response(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        async with session.post(API_URL, headers=HEADERS, json=payload) as resp:
            data = await resp.json()
            try:
                return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return f"❌ AI Error: {str(e)}"
