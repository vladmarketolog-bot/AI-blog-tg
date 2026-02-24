import time
import random
from datetime import datetime, timedelta
from .utils import get_weekly_digest_entries
from .ai_engine import call_gemini_api, MODEL_NAMES
from .publisher import send_post


DIGEST_PROMPT = """
Ты — редактор Telegram-канала для инди-хакеров и No-code билдеров.

Тебе дан список статей, опубликованных за неделю. Для каждой статьи напиши ровно 1 строку — краткий, живой анонс без воды.

Формат для каждой статьи:
→ [одна строка сути, 10-15 слов. Цифры приветствуются. Без "уникальный", "потрясающий"]

Верни только аннотации в нужном порядке, без лишних слов.
"""


def _get_week_range_str():
    """Returns a human-readable week range string, e.g. '17–23 февраля'."""
    today = datetime.utcnow()
    start = today - timedelta(days=6)
    months = [
        "", "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    if start.month == today.month:
        return f"{start.day}–{today.day} {months[today.month]}"
    return f"{start.day} {months[start.month]} – {today.day} {months[today.month]}"


def _generate_annotations(entries):
    """Asks AI to generate one-line annotations for each entry."""
    articles_text = "\n".join(
        [f"{i+1}. {e['title']}" for i, e in enumerate(entries)]
    )
    prompt = f"{DIGEST_PROMPT}\n\nСписок статей:\n{articles_text}"

    models = MODEL_NAMES.copy()
    random.shuffle(models)

    for model in models:
        result = call_gemini_api(model, prompt)
        if result:
            return result.strip()

    return None


def _number_emoji(n):
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    return emojis[n - 1] if 1 <= n <= 10 else f"{n}."


def build_and_send_digest():
    """
    Collects published posts from the last 7 days and sends a weekly digest
    to the Telegram channel.
    """
    print("📬 Building weekly digest...")
    entries = get_weekly_digest_entries()

    if len(entries) < 2:
        print(f"Not enough articles for digest ({len(entries)} found). Skipping.")
        return False

    print(f"Found {len(entries)} articles for this week's digest.")

    # Generate AI annotations
    print("Generating AI annotations...")
    annotations_raw = _generate_annotations(entries)

    # Parse annotation lines (one per entry)
    if annotations_raw:
        lines = [l.strip().lstrip("→").strip() for l in annotations_raw.splitlines() if l.strip()]
        # Pad or trim to match entry count
        while len(lines) < len(entries):
            lines.append("Интересный кейс — читай по ссылке.")
        lines = lines[:len(entries)]
    else:
        lines = ["Интересный кейс — читай по ссылке."] * len(entries)

    # Build the digest post
    week_str = _get_week_range_str()
    header = f"📬 *Дайджест недели | {week_str}*\n\nЗа эту неделю разобрали {len(entries)} кейс{'а' if 2 <= len(entries) <= 4 else 'ов'} для инди-хакеров:\n"

    items = []
    for i, (entry, annotation) in enumerate(zip(entries, lines), start=1):
        emoji = _number_emoji(i)
        title = entry["title"]
        url = entry["url"]
        items.append(f"{emoji} *{title}*\n   {annotation}\n   [Читать]({url})")

    footer = "\n\n#дайджест #nocode #microsaas #индихакер"
    post = header + "\n\n".join(items) + footer

    print("Sending digest to channel...")
    success = send_post(post, None)

    if success:
        print(f"✅ Weekly digest sent successfully ({len(entries)} articles).")
    else:
        print("❌ Failed to send weekly digest.")

    return success
