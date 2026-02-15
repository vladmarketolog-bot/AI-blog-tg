from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

TEMPLATE_PATH = "template.png"
COVER_OUTPUT = "cover.jpg"

def create_cover(title, tools, revenue=""):
    """
    Generates a cover image based on the template with metrics overlay.
    """
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Template not found at {TEMPLATE_PATH}. Skipping image generation.")
        return None

    try:
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Load font - try to load a system font or default
        try:
             # Try standard fonts
            title_font = ImageFont.truetype("arial.ttf", 60)
            tools_font = ImageFont.truetype("arial.ttf", 40)
            metric_font = ImageFont.truetype("arialbd.ttf", 50)  # Bold for metrics
            metric_label_font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            title_font = ImageFont.load_default()
            tools_font = ImageFont.load_default()
            metric_font = ImageFont.load_default()
            metric_label_font = ImageFont.load_default()

        # Draw Title (Centered)
        lines = textwrap.wrap(title, width=20)
        
        y_text = height / 2 - (len(lines) * 35)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text(((width - text_width) / 2, y_text), line, font=title_font, fill="white")
            y_text += text_height + 10

        # Draw Tools (Bottom)
        tools_text = f"Tools: {tools}"
        bbox = draw.textbbox((0, 0), tools_text, font=tools_font)
        text_width = bbox[2] - bbox[0]
        x_tools = (width - text_width) / 2
        y_tools = height - 100
        
        draw.text((x_tools, y_tools), tools_text, font=tools_font, fill="white")

        # Draw Metrics Card (Top-Right Corner) if revenue exists
        if revenue:
            card_width = 280
            card_height = 100
            card_x = width - card_width - 30
            card_y = 30
            
            # Semi-transparent background
            overlay = Image.new('RGBA', (card_width, card_height), (0, 0, 0, 180))
            img.paste(overlay, (card_x, card_y), overlay)
            
            # Draw revenue text
            draw.text((card_x + 20, card_y + 20), "💰", font=metric_font, fill="white")
            draw.text((card_x + 90, card_y + 30), revenue, font=metric_label_font, fill="#00ff88")

        img = img.convert("RGB")
        img.save(COVER_OUTPUT)
        print(f"Cover image saved to {COVER_OUTPUT}")
        return COVER_OUTPUT

    except Exception as e:
        print(f"Error creating cover: {e}")
        return None
