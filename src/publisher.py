import requests
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
import os

def send_post(text, image_path):
    """
    Sends the post to the Telegram channel.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        print("Telegram credentials missing. Skipping publish.")
        return False

    url_photo = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    try:
        # Prepare payload
        data = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "caption": text,
            "parse_mode": "Markdown" 
        }
        
        # Send with image
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                files = {"photo": f}
                response = requests.post(url_photo, data=data, files=files)
        else:
             # Just text? The prompt implies image is required for score >= 8
            print("Image path missing for send_post. Sending text only (fallback).")
            url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
            response = requests.post(url_msg, data=data)

        if response.status_code == 200:
            print("Post published successfully.")
            return True
        else:
            print(f"Failed to publish post: {response.text}")
            return False

    except Exception as e:
        print(f"Error publishing post: {e}")
        return False
