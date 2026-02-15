from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

TEMPLATE_PATH = "template.png"
COVER_OUTPUT = "cover.jpg"

def create_cover(title, tools):
    """
    Generates a cover image based on the template.
    """
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Template not found at {TEMPLATE_PATH}. Skipping image generation.")
        return None

    try:
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Configuration for text (approximate, adjust based on your template)
        # Assuming we need to center the title and put tools at the bottom
        
        # Load font - try to load a system font or default
        try:
             # Try standard fonts
            title_font = ImageFont.truetype("arial.ttf", 60)
            tools_font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            # Fallback to default load_default() which is very small, so we might need better fallback
            # But usually arial.ttf is available on Windows/Linux containers
            title_font = ImageFont.load_default()
            tools_font = ImageFont.load_default()

        # Draw Title (Centered)
        # Wrap text
        lines = textwrap.wrap(title, width=20) # Adjust width based on font size and image width
        
        y_text = height / 2 - (len(lines) * 35) # Approximate logical centering
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
        y_tools = height - 100 # 100px from bottom
        
        draw.text((x_tools, y_tools), tools_text, font=tools_font, fill="white")

        img = img.convert("RGB") # Ensure RGB for JPEG
        img.save(COVER_OUTPUT)
        print(f"Cover image saved to {COVER_OUTPUT}")
        return COVER_OUTPUT

    except Exception as e:
        print(f"Error creating cover: {e}")
        return None
