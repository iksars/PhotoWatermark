
import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import piexif

def get_shooting_date(image_path):
    """Extracts the shooting date from the image's EXIF data."""
    try:
        exif_dict = piexif.load(image_path)
        if piexif.ImageIFD.DateTime in exif_dict["Exif"]:
            date_str = exif_dict["Exif"][piexif.ImageIFD.DateTime].decode("utf-8")
            return date_str.split(" ")[0].replace(":", "-")
    except Exception as e:
        print(f"Could not read EXIF data from {image_path}: {e}")
    return None

def add_watermark(image_path, text, output_path, font_size, color, position):
    """Adds a text watermark to an image."""
    try:
        image = Image.open(image_path).convert("RGBA")
        txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
            print("Arial font not found. Using default font.")

        draw = ImageDraw.Draw(txt_layer)
        
        # Get text size using textbbox
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = 0, 0
        if position == "top-left":
            x, y = 10, 10
        elif position == "center":
            x = (image.width - text_width) / 2
            y = (image.height - text_height) / 2
        elif position == "bottom-right":
            x = image.width - text_width - 10
            y = image.height - text_height - 10

        draw.text((x, y), text, font=font, fill=color)
        
        watermarked_image = Image.alpha_composite(image, txt_layer)
        watermarked_image = watermarked_image.convert("RGB") # Convert back to RGB before saving
        watermarked_image.save(output_path, "JPEG")
        print(f"Watermarked image saved to {output_path}")

    except Exception as e:
        print(f"Failed to add watermark to {image_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Add a date watermark to images.")
    parser.add_argument("image_dir", type=str, help="Directory containing the images.")
    parser.add_argument("--font-size", type=int, default=50, help="Font size of the watermark text.")
    parser.add_argument("--color", type=str, default="white", help="Color of the watermark text.")
    parser.add_argument("--position", type=str, default="bottom-right", 
                        choices=["top-left", "center", "bottom-right"],
                        help="Position of the watermark.")

    args = parser.parse_args()

    if not os.path.isdir(args.image_dir):
        print(f"Error: Directory not found at {args.image_dir}")
        return

    output_dir = os.path.join(args.image_dir, os.path.basename(args.image_dir) + "_watermark")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(args.image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(args.image_dir, filename)
            
            date_str = get_shooting_date(image_path)
            if not date_str:
                date_str = "No Date"

            output_filename = os.path.splitext(filename)[0] + "_watermarked.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            add_watermark(image_path, date_str, output_path, args.font_size, args.color, args.position)

if __name__ == "__main__":
    main()
