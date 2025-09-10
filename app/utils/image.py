"""
Image processing utilities for the CultivAR application.
"""

import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from app.logger import logger


def save_image(image_file, upload_folder, filename=None):
    """
    Save an uploaded image to the specified folder with security validation.

    Args:
        image_file: The uploaded image file.
        upload_folder (str): The folder to save the image to.
        filename (str, optional): The filename to use. If None, a timestamp will be used.

    Returns:
        str: The path to the saved image.
    """
    try:
        if not image_file or not image_file.filename:
            logger.error("No image file provided")
            return None

        # Validate file size
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
        image_file.seek(0, 2)  # Seek to end
        file_size = image_file.tell()
        image_file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            logger.error(f"File size {file_size} exceeds 10MB limit")
            return None

        # Validate file type
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        ALLOWED_MIMETYPES = {
            'image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp'
        }
        
        original_filename = image_file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
        
        if file_extension not in ALLOWED_EXTENSIONS:
            logger.error(f"Invalid file extension: {file_extension}")
            return None
            
        if hasattr(image_file, 'mimetype') and image_file.mimetype not in ALLOWED_MIMETYPES:
            logger.error(f"Invalid file mimetype: {image_file.mimetype}")
            return None

        # Create the upload folder if it doesn't exist
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Generate a filename if one wasn't provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            from werkzeug.utils import secure_filename
            secure_name = secure_filename(original_filename)
            filename = f"{timestamp}_{secure_name}"
        
        # Ensure filename is secure
        from werkzeug.utils import secure_filename
        filename = secure_filename(filename)

        # Save the image
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)

        # Validate the saved file is actually an image
        try:
            with Image.open(image_path) as img:
                img.verify()  # Verify it's a valid image
        except Exception as e:
            # Remove the uploaded file if it's not a valid image
            if os.path.exists(image_path):
                os.remove(image_path)
            logger.error(f"Uploaded file is not a valid image: {e}")
            return None

        return image_path
    except Exception as e:
        logger.error(f"Error saving image: {e}")
        return None


def decorate_image(image_path, text, font_path=None, font_size=36, position="bottom"):
    """
    Add text to an image.

    Args:
        image_path (str): The path to the image.
        text (str): The text to add to the image.
        font_path (str, optional): The path to the font to use.
        font_size (int, optional): The font size to use.
        position (str, optional): The position to place the text ('top', 'bottom', 'center').

    Returns:
        str: The path to the decorated image.
    """
    try:
        # Open the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        # Load the font
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        # Calculate text size
        text_width, text_height = draw.textsize(text, font=font)

        # Calculate text position
        if position == "top":
            text_position = ((img.width - text_width) // 2, 10)
        elif position == "center":
            text_position = (
                (img.width - text_width) // 2,
                (img.height - text_height) // 2,
            )
        else:  # bottom
            text_position = (
                (img.width - text_width) // 2,
                img.height - text_height - 10,
            )

        # Add text to image
        draw.text(text_position, text, font=font, fill=(255, 255, 255))

        # Save the decorated image
        decorated_path = f"{os.path.splitext(image_path)[0]}_decorated{os.path.splitext(image_path)[1]}"
        img.save(decorated_path)

        return decorated_path
    except Exception as e:
        logger.error(f"Error decorating image: {e}")
        return None
