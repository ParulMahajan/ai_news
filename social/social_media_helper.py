import os
import tempfile
from social._facebook import post_to_facebook
from social.instagram import post_to_instagram
from social.linkedin import post_to_linkedin
from utils.logger import logger

def post_to_social_media(title, summary, image_bytes, hashtag):

    results = {}

    # Validate inputs
    if not title or not summary:
        logger.error("Title and summary are required")
        return None

    try:
        formatted_message = format_post_content(summary)

        # Create temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(image_bytes)
            temp_file.flush()
            temp_path = temp_file.name

        # Post to facebook
        results["facebook"] = post_to_facebook(temp_path, title, summary, hashtag)

        # Post to instagram
        results["instagram"] = post_to_instagram(image_bytes, formatted_message, hashtag)

        # Post to LinkedIn
        results["linkedin"] = post_to_linkedin(temp_path, formatted_message, hashtag)

        return results

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def format_post_content(summary):

    # Add CTA (Call to Action)
    cta = "🔔 Follow us for daily AI updates!"

    separator = "\n\n"
    return f"{summary}{separator}{cta}"


