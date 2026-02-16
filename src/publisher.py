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
            # Check caption length (Telegram limit is 1024 chars)
            if len(text) > 1000:
                # Send photo with short caption, then text
                short_caption = text[:1000] + "..."
                with open(image_path, "rb") as f:
                    files = {"photo": f}
                    # Send photo first (no caption or short caption if we wanted, but let's just send text separately)
                    # Actually, better UX: Send photo with no caption, then full text.
                    # Or: Send photo with title, then body.
                    # Let's go with: Photo + "New Post below" -> Text
                    
                    requests.post(url_photo, data={"chat_id": TELEGRAM_CHANNEL_ID}, files=files)
                
                # Send full text as separate message (limit 4096)
                url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                data = {"chat_id": TELEGRAM_CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
                response = requests.post(url_msg, data=data)
            else:
                # Normal photo + caption
                with open(image_path, "rb") as f:
                    files = {"photo": f}
                    response = requests.post(url_photo, data=data, files=files)
        else:
             # Just text? The prompt implies image is required for score >= 8
            print("Sending text only (Image generation disabled).")
            url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            # Explicitly enable link previews (disable_web_page_preview=False)
            data = {
                "chat_id": TELEGRAM_CHANNEL_ID, 
                "text": text, 
                "parse_mode": "Markdown",
                "disable_web_page_preview": False 
            }
            response = requests.post(url_msg, data=data)

        if response.status_code == 200:
            print("Post published successfully.")
            return True
        else:
            print(f"Failed to publish post (Markdown error?): {response.text}")
            # FALLBACK: Try sending without Markdown
            if "can't parse entities" in response.text or "Bad Request" in response.text:
                print("⚠️ Markdown parsing failed. Retrying as plain text...")
                data.pop("parse_mode", None) # Remove parse_mode completely
                response_fallback = requests.post(url_msg, data=data)
                if response_fallback.status_code == 200:
                     print("Post published successfully (Plain Text Fallback).")
                     return True
                else:
                    print(f"Failed to publish even as plain text: {response_fallback.text}")
                    return False
            return False

    except Exception as e:
        print(f"Error publishing post: {e}")
        return False
