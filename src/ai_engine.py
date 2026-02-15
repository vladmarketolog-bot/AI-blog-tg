import google.generativeai as genai
import os
from .config import WRITER_PROMPT, CRITIC_PROMPT, GEMINI_API_KEY

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAMES = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]

def generate_post(article_text):
    """
    Generates a draft post using Gemini, trying multiple models.
    """
    for model_name in MODEL_NAMES:
        try:
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{WRITER_PROMPT}\n\nТекст статьи:\n{article_text}"
            response = model.generate_content(full_prompt)
            print(f"Successfully generated using {model_name}")
            return response.text.strip()
        except Exception as e:
            print(f"Error generating post with {model_name}: {e}")
            continue
    
    print("All models failed to generate post.")
    return None

def critique_post(draft_post):
    """
    Critiques the draft post and returns a score (0-10).
    """
    for model_name in MODEL_NAMES:
        try:
            model = genai.GenerativeModel(model_name)
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
            print(f"Error critiquing post with {model_name}: {e}")
            continue
            
    print("All models failed to critique post.")
    return 0
