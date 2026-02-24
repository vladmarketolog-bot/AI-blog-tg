import json
import os
from datetime import datetime, timedelta

HISTORY_FILE = "history.json"
DIGEST_FILE = "digest.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def is_url_processed(url):
    history = load_history()
    return url in history

def add_url_to_history(url):
    history = load_history()
    if url not in history:
        history.append(url)
        save_history(history)

# --- Digest helpers ---

def load_digest():
    if not os.path.exists(DIGEST_FILE):
        return []
    try:
        with open(DIGEST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_digest(digest):
    with open(DIGEST_FILE, "w", encoding="utf-8") as f:
        json.dump(digest, f, indent=4, ensure_ascii=False)

def add_to_digest(title, url):
    """Records a published post for the weekly digest."""
    digest = load_digest()
    entry = {
        "title": title,
        "url": url,
        "published_at": datetime.utcnow().strftime("%Y-%m-%d")
    }
    digest.append(entry)
    save_digest(digest)

def get_weekly_digest_entries():
    """Returns all digest entries published in the last 7 days."""
    digest = load_digest()
    cutoff = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    return [e for e in digest if e.get("published_at", "") >= cutoff]
