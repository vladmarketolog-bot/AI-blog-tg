import requests
import json
import re
from .config import WRITER_PROMPT, CRITIC_PROMPT, GEMINI_API_KEY

# Verified models from API check
# gemini-flash-latest showed success in logs, prioritizing it
MODEL_NAMES = ["gemini-flash-latest", "gemini-2.0-flash-lite", "gemini-2.0-flash"]

import time

def call_gemini_api(model_name, prompt):
    """
    Calls the Gemini REST API directly with robust error handling.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    max_retries = 3  # Increase to 3 for reliability
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            # Handle Rate Limiting (429)
            if response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 30 * (attempt + 1) # 30s, 60s
                    print(f"Rate limit hit for {model_name}. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Rate limit hit for {model_name}. Trying next model...")
                    return None
                
            response.raise_for_status()
            result = response.json()
            
            # Extract text from response
            if 'candidates' in result and result['candidates']:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return content
            else:
                print(f"Unexpected response format from {model_name}: {result}")
                return None
                
        except Exception as e:
            print(f"Error calling {model_name} (Attempt {attempt+1}/{max_retries}): {e}")
            try:
                # Check if response object exists before accessing status_code
                if 'response' in locals() and response.status_code != 200:
                     print(f"Response: {response.text}")
            except:
                pass
            
            # Don't retry on client errors (400, 404, etc) except 429 which is handled above
            if 'response' in locals() and 400 <= response.status_code < 500 and response.status_code != 429:
                return None
            
            # Retry on server errors or connection issues
            time.sleep(5)
            
    print(f"Failed to generate with {model_name} after {max_retries} attempts.")
    return None

def generate_post(article_text):
    """
    Generates a draft post using Gemini, trying multiple models via REST API.
    """
    for model_name in MODEL_NAMES:
        full_prompt = f"{WRITER_PROMPT}\n\nТекст статьи:\n{article_text}"
        result = call_gemini_api(model_name, full_prompt)
        if result:
            print(f"Successfully generated using {model_name}")
            return result.strip()
            
    print("All models failed to generate post.")
    return None

def critique_post(draft_post):
    """
    Critiques the draft post and returns a score (0-10).
    """
    for model_name in MODEL_NAMES:
        full_prompt = f"{CRITIC_PROMPT}\n\nЧерновик поста:\n{draft_post}"
        result = call_gemini_api(model_name, full_prompt)
        if result:
            text_score = result.strip()
            # Parse the score
            # Parse the score
            match = re.search(r'\d+', text_score)
            if match:
                score = int(match.group())
                if 0 <= score <= 10:
                    return score
                # If score is somehow > 10 (e.g. 1000/10), it's likely a parsing error or hallucination.
                # Return 0 to be safe
                return 0
            return 0
            
    print("All models failed to critique post.")
    return 0
