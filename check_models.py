import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def list_models():
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print("Available Models:")
        if 'models' in data:
            for model in data['models']:
                print(f"- {model['name']}")
                print(f"  Supported methods: {model.get('supportedGenerationMethods', [])}")
        else:
            print("No models found in response.")
            print(data)
            
    except requests.exceptions.RequestException as e:
        print(f"Error listing models: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")

if __name__ == "__main__":
    list_models()
