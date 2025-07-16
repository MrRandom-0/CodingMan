# === utils/users.py ===

import json
import os

DATA_DIR = "data"
BOOKMARK_FILE = os.path.join(DATA_DIR, "bookmarks.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_bookmarks():
    if not os.path.exists(BOOKMARK_FILE):
        return {}
    with open(BOOKMARK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_bookmarks(data):
    with open(BOOKMARK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_bookmark(user_id, challenge_text):
    bookmarks = load_bookmarks()
    bookmarks.setdefault(str(user_id), []).append(challenge_text)
    save_bookmarks(bookmarks)

def get_bookmarks(user_id):
    bookmarks = load_bookmarks()
    return bookmarks.get(str(user_id), [])

# Add this at the bottom of utils/users.py (after bookmarks logic)

PROFILE_FILE = os.path.join(DATA_DIR, "profiles.json")

def load_profiles():
    if not os.path.exists(PROFILE_FILE):
        return {}
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profiles(data):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_user_profile(user_id):
    profiles = load_profiles()
    return profiles.get(str(user_id), {
        "xp": 0,
        "level": 1,
        "rank": "Unranked"
    })

def save_user_profile(user_id, data):
    profiles = load_profiles()
    profiles[str(user_id)] = data
    save_profiles(profiles)
