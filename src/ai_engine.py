import google.generativeai as genai
import os
from .config import WRITER_PROMPT, CRITIC_PROMPT, GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"

def generate_post(article_text):
    """
    Generates a draft post using Gemini 1.5 Pro.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        full_prompt = f"{WRITER_PROMPT}\n\nТекст статьи:\n{article_text}"
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating post: {e}")
        return None

def critique_post(draft_post):
    """
    Critiques the draft post and returns a score (0-10).
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        full_prompt = f"{CRITIC_PROMPT}\n\nЧерновик поста:\n{draft_post}"
        response = model.generate_content(full_prompt)
        text_score = response.text.strip()
        
        # Parse the score - sometimes the model outputs text like "Score: 8" instead of just "8"
        import re
        match = re.search(r'\d+', text_score)
        if match:
            return int(match.group())
        return 0
    except Exception as e:
        print(f"Error critiquing post: {e}")
        return 0
