import io
from PIL import Image

def compress_image(image_data):
    """Compress image only if it exceeds Facebook's 4MB limit"""
    # Check original size
    original_size_mb = len(image_data) / (1024 * 1024)

    # Only compress if larger than 4MB
    if original_size_mb <= 4:
        return image_data

    img = Image.open(io.BytesIO(image_data))

    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    quality = 95
    while True:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality)
        size_mb = len(buffer.getvalue()) / (1024 * 1024)

        if size_mb <= 3.9 or quality <= 5:
            logger.info(f"Compressed image from {original_size_mb:.2f}MB to {size_mb:.2f}MB")
            return buffer.getvalue()

        quality -= 5