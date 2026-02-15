import json
import os

HISTORY_FILE = "history.json"

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
