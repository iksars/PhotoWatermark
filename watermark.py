import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import piexif

def get_shooting_date(image_path):
    """Extracts the shooting date from the image's EXIF data."""
    try:
        exif_dict = piexif.load(image_path)
        date_str = None
        
        # Prioritize DateTimeOriginal from the Exif block
        if "Exif" in exif_dict and exif_dict["Exif"] and piexif.ExifIFD.DateTimeOriginal in exif_dict["Exif"]:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
        # Fallback to DateTimeDigitized
        elif "Exif" in exif_dict and exif_dict["Exif"] and piexif.ExifIFD.DateTimeDigitized in exif_dict["Exif"]:
            date_str = exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized].decode("utf-8")
        # Fallback to the general DateTime tag
        elif "0th" in exif_dict and exif_dict["0th"] and piexif.ImageIFD.DateTime in exif_dict["0th"]:
            date_str = exif_dict["0th"][piexif.ImageIFD.DateTime].decode("utf-8")

        if date_str:
            return date_str.split(" ")[0].replace(":", "-")
            
    except Exception as e:
        print(f"Could not read EXIF data from {image_path}: {e}")
    return None

def add_watermark(image_path, text, output_path, font_size, color, position, font_path):
    """Adds a text watermark to an image."""
    try:
        image = Image.open(image_path)

        # Check for and apply EXIF orientation
        try:
            exif_dict = piexif.load(image.info['exif'])
            if piexif.ImageIFD.Orientation in exif_dict['0th']:
                orientation = exif_dict['0th'].pop(piexif.ImageIFD.Orientation)
                if orientation == 2:
                    image = image.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    image = image.rotate(180)
                elif orientation == 4:
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                elif orientation == 5:
                    image = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    image = image.rotate(-90, expand=True)
                elif orientation == 7:
                    image = image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except (KeyError, AttributeError, TypeError, piexif.InvalidImageDataError):
            # Cases: image has no exif, exif has no orientation, or other errors
            pass

        image = image.convert("RGBA")
        txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        
        try:
            font_to_use = font_path
            if not font_to_use:
                # Default to the font file in the 'fonts' directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                font_to_use = os.path.join(script_dir, "fonts", "Roboto-Regular.ttf")

            font = ImageFont.truetype(font_to_use, font_size)
        except IOError:
            font = ImageFont.load_default()
            if font_path:
                print(f"Font not found at {font_path}. Using default font (font size may not apply).")
            else:
                print("Default font 'Roboto-Regular.ttf' not found in 'fonts' folder. Using default font (font size may not apply).")

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
    parser.add_argument("--font-path", type=str, default=None, help="Path to a .ttf or .otf font file.")

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
            
            add_watermark(image_path, date_str, output_path, args.font_size, args.color, args.position, args.font_path)

if __name__ == "__main__":
    main()
