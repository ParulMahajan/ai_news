import os
import requests
import tempfile
from social._facebook import post_to_facebook
from facebook import GraphAPI
from social.instagram import post_to_instagram
from social.linkedin import post_to_linkedin_with_image
from utils.logger import logger
# from dotenv import load_dotenv
# load_dotenv()



def post_to_social_media(title, summary, image_bytes):

    results = {}

    # Validate inputs
    if not title or not summary:
        logger.error("Title and summary are required")
        return None

    try:
        formatted_message = format_post_content(title, summary)

        # Validate message length (Facebook limit is 63206 characters)
        if len(formatted_message) > 63000:
            logger.error("Message too long for Facebook")
            formatted_message = formatted_message[:63000]

        # Create temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_file.flush()
            temp_path = temp_file.name

        # Post to facebook
        results["facebook"] = post_to_facebook(temp_path, formatted_message)

        # Post to instagram
        results["instagram"] = post_to_instagram(image_bytes, formatted_message)

        # Post to LinkedIn
        results["linkedin"] = post_to_linkedin_with_image(temp_path, formatted_message)

        return results


    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def format_post_content(title, summary):
    bold_title = to_unicode_bold(title)
    bold_summary_heading = to_unicode_bold("Key Summary")
    # Add hashtags for better reach
    hashtags = "#AI #ArtificialIntelligence #Tech #Innovation"
    # Add CTA (Call to Action)
    cta = "🔔 Follow us for daily AI updates!"

    separator = "\n \n"
    return f"{bold_title}{separator}{bold_summary_heading}:\n\n{summary}\n\n{hashtags}\n\n{cta}"

def to_unicode_bold(text):
    bold_map = {chr(i): chr(i + 0x1D400 - 0x41) for i in range(0x41, 0x5A + 1)}  # A-Z
    bold_map.update({chr(i): chr(i + 0x1D41A - 0x61) for i in range(0x61, 0x7A + 1)})  # a-z
    return ''.join(bold_map.get(c, c) for c in text)

