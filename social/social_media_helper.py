import os
import requests
import tempfile
from facebook import GraphAPI, GraphAPIError  # Import GraphAPI directly from facebook module
from utils.image import compress_image
from utils.logger import logger


def post_to_social_media(title, summary, image_url):
    access_token = os.getenv("FB_ACCESS_TOKEN")
    instagram_account_id = os.getenv("IG_ACCOUNT_ID")
    graph = GraphAPI(access_token)
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

        if not image_url or not image_url.strip():
            logger.error("Facebook requires an image for posting")
            return None

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            logger.error(f"Failed to download image: {image_response.status_code}")
            return None

        # Validate image type
        content_type = image_response.headers.get('content-type', '')
        supported_types = ('image/jpeg', 'image/png', 'image/jpg')

        if not content_type.startswith(supported_types):
            logger.error(f"Invalid image type: {content_type} for URL: {image_url}")
            # Try to get a different image if available
            if 'favicon' in image_url.lower() or '.ico' in image_url.lower():
                logger.error("Favicon detected - this type of image is not supported for Facebook posts")
            return None

        # Compress only if needed
        try:
            image_data = compress_image(image_response.content)
        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            return None

        # Create temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file.flush()
            temp_path = temp_file.name

        try:
            # Post to facebook
            with open(temp_path, 'rb') as image_file:
                results['facebook'] = graph.put_photo(
                    image=image_file,
                    message=formatted_message,
                    published=True
                )

            #Post to Instagram
            with open(temp_path, 'rb') as image_file:
                container = graph.put_object(
                    instagram_account_id,
                    "media",
                    image_url=image_url,  # Use image file directly
                    media_type="IMAGE",
                    caption=formatted_message[:2200], #title

                )
            import time
            if container and 'id' in container:
                time.sleep(5)  # Wait for container processing
                results['instagram'] = graph.put_object(
                    instagram_account_id,
                    "media_publish",
                    creation_id=container['id']
                )
            else:
                logger.error("Instagram container creation failed")

            return results

        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except GraphAPIError as e:
        logger.error(f"Facebook posting error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None

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

def get_long_lived_token():
    """Convert short-lived token to long-lived token"""
    app_id = os.getenv("FB_APP_ID")
    app_secret = os.getenv("FB_APP_SECRET")
    short_lived_token = os.getenv("FB_ACCESS_TOKEN")

    graph = GraphAPI(access_token=short_lived_token,version="3.1")
    try:
        # Exchange tokens using the correct endpoint
        response = graph.extend_access_token(app_id, app_secret)
        return response['access_token']
    except GraphAPIError as e:
        print(f"Error exchanging token: {e}")
        return None

def get_permanent_page_token():
    """Get permanent page access token"""
    user_token = get_long_lived_token()
    if not user_token:
        return None
    graph = GraphAPI(user_token, version="3.1")
    page_id = os.getenv("FB_PAGE_ID")
    try:
        pages = graph.get_object('me/accounts')
        for page in pages['data']:
            if page['id'] == page_id:
                return page['access_token']
        return None
    except GraphAPIError as e:
        print(f"Error getting page token: {e}")
        return None


def delete_all_posts():
    """Delete all posts from the Facebook page"""
    access_token = os.getenv("FB_ACCESS_TOKEN")
    page_id = os.getenv("FB_PAGE_ID")
    graph = GraphAPI(access_token)

    try:
        # Get posts in batches of 100
        while True:
            # Get posts from the page
            posts = graph.get_object(
                f"{page_id}/posts",
                fields="id",
                limit=100
            )

            if not posts['data']:
                logger.info("No more posts to delete")
                break

            # Delete each post
            for post in posts['data']:
                try:
                    graph.delete_object(post['id'])
                    logger.info(f"Deleted post {post['id']}")
                except GraphAPIError as e:
                    logger.error(f"Error deleting post {post['id']}: {str(e)}")
                    continue

    except GraphAPIError as e:
        logger.error(f"Error fetching posts: {str(e)}")
        return False

    return True

# permToken = get_permanent_page_token()
# print(f"Permanent Page Token: {permToken}")

# delete_all_posts()

