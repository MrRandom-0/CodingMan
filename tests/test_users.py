"""Tests for the pure user-store helpers in utils/users.py.

The store's file paths are module globals, so each test points them at a
tmp_path file first — the real data/ directory is never touched.
"""

import pytest

import utils.users as users


@pytest.fixture(autouse=True)
def isolate_store(tmp_path, monkeypatch):
    monkeypatch.setattr(users, "BOOKMARK_FILE", str(tmp_path / "bookmarks.json"))
    monkeypatch.setattr(users, "PROFILE_FILE", str(tmp_path / "profiles.json"))


def test_missing_files_load_as_empty():
    assert users.load_bookmarks() == {}
    assert users.load_profiles() == {}
    assert users.get_bookmarks(123) == []


def test_bookmark_roundtrip_per_user():
    users.save_bookmark(42, "Reverse a linked list")
    users.save_bookmark(42, "Binary search")
    users.save_bookmark(7, "Two sum")
    assert users.get_bookmarks(42) == ["Reverse a linked list", "Binary search"]
    assert users.get_bookmarks(7) == ["Two sum"]
    assert users.get_bookmarks(999) == []


def test_default_profile_for_new_user():
    assert users.get_user_profile(555) == {"xp": 0, "level": 1, "rank": "Unranked"}


def test_profile_roundtrip():
    users.save_user_profile(42, {"xp": 250, "level": 3, "rank": "Silver"})
    assert users.get_user_profile(42) == {"xp": 250, "level": 3, "rank": "Silver"}
    # Other users still get the default.
    assert users.get_user_profile(43)["xp"] == 0
