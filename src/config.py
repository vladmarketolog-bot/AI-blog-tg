import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

RSS_FEEDS = [
    "https://www.reddit.com/r/nocode/.rss",
    "https://www.reddit.com/r/saas/.rss",
    "https://www.indiehackers.com/feed"
]

# Prompt for the Writer
WRITER_PROMPT = """
Ты — CTO и эксперт по микро-бизнесу. Твоя задача: превратить этот текст в пост для Telegram в стиле 'минимализм'.
Структура:

Название проекта (жирным).

Суть: Одно предложение, ЧТО делает продукт.

Стек: Найди или предположи No-code стек (Bubble, Make и т.д.).

Профит: Сколько заработали/какой рост (в $/мес).

Инсайт: 1 предложение, почему это сработало (маркетинговая фишка).
Запрещено: Вода, хвалебные эпитеты, приветствия.
"""

# Prompt for the Critic
CRITIC_PROMPT = """
Оцени этот пост по шкале 1–10.
Давай баллы только за:

Конкретные цифры денег/роста (3 балла).

Понятный стек инструментов (3 балла).

Отсутствие 'воды' и общих фраз (2 балла).

Четкий, полезный инсайт (2 балла).
Верни только число.
"""
