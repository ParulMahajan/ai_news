from model.llm import  google_client
from utils.logger import logger
from PIL import Image
from io import BytesIO

def generate_image(prompt: str) -> bytes:
    response = google_client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[prompt],
    )

    for part in response.candidates[0].content.parts:
        if part.text is not None:
            logger.info(part.text)
        elif part.inline_data is not None:
            # Open image from binary data
            ai_image = Image.open(BytesIO(part.inline_data.data))
            # Save locally if needed
            ai_image.save("generated_image.jpeg")

            # Convert PIL Image to raw bytes for direct use
            buf = BytesIO()
            ai_image.save(buf, format="PNG")  # or "JPEG"
            image_bytes = buf.getvalue()
            logger.info("Image created successfully")
            return image_bytes
        else:
            logger.error("Image generation failed")
            return None
    else:
        logger.error("No valid content in response from AI for image generation")
        return None