from PIL import Image, ImageDraw, ImageFont

def create_template():
    # Create a simple dark background template
    width, height = 1080, 1080
    color = (20, 20, 20)  # Dark gray/black
    img = Image.new('RGB', (width, height), color)
    
    # Optional: Add some minimal design elements if needed, but for now just a solid color 
    # as the prompt says "text on template". 
    # Let's add a subtle border or something to make it look "minimalist" but designed.
    draw = ImageDraw.Draw(img)
    border_color = (255, 255, 255)
    border_width = 10
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], outline=border_color, width=2)

    img.save("template.png")
    print("template.png created")

if __name__ == "__main__":
    create_template()
